import re
import sys

from pystratum.RoutineLoaderHelper import RoutineLoaderHelper
from pystratum.mssql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlRoutineLoaderHelper(RoutineLoaderHelper):
    """
    Class for loading a single stored routine into a SQL Server instance from a (pseudo) SQL file.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 routine_filename,
                 routine_file_encoding,
                 pystratum_old_metadata,
                 replace_pairs,
                 rdbms_old_metadata):
        """
        Object constructor.

        :param str routine_filename: The filename of the source of the stored routine.
        :param str routine_file_encoding: The encoding of the source file.
        :param dict pystratum_old_metadata: The metadata of the stored routine from PyStratum.
        :param dict[str,str] replace_pairs: A map from placeholders to their actual values.
        :param dict rdbms_old_metadata: The old metadata of the stored routine from MS SQL Server.
        """
        RoutineLoaderHelper.__init__(self,
                                     routine_filename,
                                     routine_file_encoding,
                                     pystratum_old_metadata,
                                     replace_pairs,
                                     rdbms_old_metadata)

        self._routines_schema_name = None
        """
        The name of the schema of the stored routine.

        :type: str
        """

        self._routine_base_name = None
        """
        The name of the stored routine without schema name.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _must_reload(self):
        """
        Returns True if the source file must be load or reloaded. Otherwise returns False.

        :rtype: bool
        """
        if not self._pystratum_old_metadata:
            return True

        if self._pystratum_old_metadata['timestamp'] != self._m_time:
            return True

        if self._pystratum_old_metadata['replace']:
            for key, value in self._pystratum_old_metadata['replace'].items():
                if key.lower() not in self._replace_pairs or self._replace_pairs[key.lower()] != value:
                    return True

        if not self._rdbms_old_metadata:
            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def _get_name(self):
        """
        Extracts the name of the stored routine and the stored routine type (i.e. procedure or function) source.

        :rtype: bool
        """
        ret = True
        p = re.compile(r"create\\s+(procedure|function)\\s+(?:(\w+)\.([a-zA-Z0-9_]+))", re.IGNORECASE)
        matches = p.findall(self._routine_source_code)

        if matches:
            self._routine_type = matches[0][0].lower()
            self._routines_schema_name = matches[0][1]
            self._routine_base_name = matches[0][2]

            if self._routine_name != matches[0][1] + '.' + matches[0][2]:
                print("Error: Stored routine name '%s.%s' does not match filename in file '%s'." % (
                    matches[0][1], matches[0][2], self._source_filename))
                ret = False
        else:
            ret = False

        if not self._routine_type:
            print("Error: Unable to find the stored routine name and type in file '%s'." % self._source_filename)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _load_routine_file(self):
        """
        Loads the stored routine into the SQL Server instance.
        """
        print("Loading %s %s" % (self._routine_type, self._routine_name))

        self._set_magic_constants()

        routine_source = []
        i = 0
        for line in self._routine_source_code_lines:
            new_line = line
            self._replace['__LINE__'] = "'%d'" % (i + 1)
            for search, replace in self._replace.items():
                tmp = re.findall(search, new_line, re.IGNORECASE)
                if tmp:
                    new_line = new_line.replace(tmp[0], replace)
            routine_source.append(new_line)
            i += 1

        routine_source = "\n".join(routine_source)

        self._unset_magic_constants()

        if self._rdbms_old_metadata:
            if self._pystratum_old_metadata and self._pystratum_old_metadata['designation'] == \
                    self._pystratum_metadata['designation']:
                p = re.compile("(create\\s+(procedure|function))", re.IGNORECASE)
                matches = p.findall(routine_source)
                if matches:
                    routine_source = routine_source.replace(matches[0][0], 'alter %s' % matches[0][1])
                else:
                    print("Error: Unable to find the stored routine type in modified source of file '%s'." %
                          self._source_filename)
            else:
                self._drop_routine()

        StaticDataLayer.execute_none(routine_source)

    # ------------------------------------------------------------------------------------------------------------------
    def get_bulk_insert_table_columns_info(self):
        """
        Gets the column names and column types of the current table for bulk insert.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _get_routine_parameters_info(self):
        query = """
select par.name      parameter_name
,      typ.name      type_name
,      typ.max_length
,      typ.precision
,      typ.scale
from       sys.schemas        scm
inner join sys.all_objects    prc  on  prc.[schema_id] = scm.[schema_id]
inner join sys.all_parameters par  on  par.[object_id] = prc.[object_id]
inner join sys.types          typ  on  typ.user_type_id = par.system_type_id
where scm.name = '%s'
and   prc.name = '%s'
order by par.parameter_id""" % (self._routines_schema_name, self._routine_base_name)

        routine_parameters = StaticDataLayer.execute_rows(query)

        if len(routine_parameters) != 0:
            for routine_parameter in routine_parameters:
                if routine_parameter['parameter_name']:
                    parameter_name = routine_parameter['parameter_name'][1:]
                    value = routine_parameter['type_name']

                    self._parameters.append({'name':                       parameter_name,
                                             'data_type': routine_parameter['type_name'],
                                             'data_type_descriptor':       value})

    # ------------------------------------------------------------------------------------------------------------------
    def _get_designation_type(self):
        """
        Extracts the designation type of the stored routine.

        Returns True on success. Otherwise returns False.

        :rtype: bool
        """
        ret = True

        key = self._routine_source_code_lines.index('as')

        if key != -1:
            p = re.compile(r'\s*--\s+type:\s*(\w+)\s*(.+)?\s*', re.IGNORECASE)
            matches = p.findall(self._routine_source_code_lines[key - 1])

            if matches:
                self._designation_type = matches[0][0]
                tmp = str(matches[0][1])
                if self._designation_type == 'bulk_insert':
                    n = re.compile(r'([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_,]+)')
                    info = n.findall(tmp)

                    if not info:
                        print("Error: Expected: -- type: bulk_insert <table_name> <columns> in file '%s'." %
                              self._source_filename, file=sys.stderr)
                    self._table_name = info[0][0]
                    self._columns = str(info[0][1]).split(',')

                elif self._designation_type == 'rows_with_key' or self._designation_type == 'rows_with_index':
                    self._columns = str(matches[0][1]).split(',')
                else:
                    if matches[0][1]:
                        ret = False
        else:
            ret = False

        if not ret:
            print("Error: Unable to find the designation type of the stored routine in file '%s'." %
                  self._source_filename, file=sys.stderr)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_routine(self):
        """
        Drops the stored routine if it exists.
        """
        if self._rdbms_old_metadata:
            if self._rdbms_old_metadata['type'].strip() == 'P':
                sql = "drop procedure [%s].[%s]" % (self._rdbms_old_metadata['schema_name'], self._routine_base_name)
            elif self._rdbms_old_metadata['type'].strip() in ('FN', 'TF'):
                sql = "drop function [%s].[%s]" % (self._rdbms_old_metadata['schema_name'], self._routine_base_name)
            else:
                raise Exception("Unknown routine type '%s'." % self._rdbms_old_metadata['type'])

            StaticDataLayer.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def _update_metadata(self):
        """
        Updates the metadata of the stored routine.
        """
        # Update general metadata.
        RoutineLoaderHelper._update_metadata(self)

        # Update SQL Server specific metadata.
        self._pystratum_metadata['schema_name'] = self._routines_schema_name

        # Update SQL Server specific metadata.
        self._pystratum_metadata['routine_base_name'] = self._routine_base_name

# ----------------------------------------------------------------------------------------------------------------------
