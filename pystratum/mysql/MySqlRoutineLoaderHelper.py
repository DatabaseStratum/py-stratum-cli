import re
import sys
from pystratum.RoutineLoaderHelper import RoutineLoaderHelper
from pystratum.mysql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class MySqlRoutineLoaderHelper(RoutineLoaderHelper):
    """
    Class for loading a single stored routine into a MySQL instance from a (pseudo) SQL file.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 routine_filename: str,
                 routine_file_extension: str,
                 routine_file_encoding: str,
                 pystratum_old_metadata: dict,
                 replace_pairs: dict,
                 rdbms_old_metadata: dict,
                 sql_mode: str,
                 character_set: str,
                 collate: str):

        RoutineLoaderHelper.__init__(self,
                                     routine_filename,
                                     routine_file_extension,
                                     routine_file_encoding,
                                     pystratum_old_metadata,
                                     replace_pairs,
                                     rdbms_old_metadata)

        self._sql_mode = sql_mode
        """
        The SQL mode under which the stored routine will be loaded and run.

        :type : string
        """

        self._character_set = character_set
        """
        The default character set under which the stored routine will be loaded and run.

        :type : string
        """

        self._collate = collate
        """
        The default collate under which the stored routine will be loaded and run.

        :type : string
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _must_reload(self) -> bool:
        """
        Returns True if the source file must be load or reloaded. Otherwise returns False.
        :return bool
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

        if self._rdbms_old_metadata['sql_mode'] != self._sql_mode:
            return True

        if self._rdbms_old_metadata['character_set_client'] != self._character_set:
            return True

        if self._rdbms_old_metadata['collation_connection'] != self._collate:
            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def _get_name(self) -> bool:
        """
        Extracts the name of the stored routine and the stored routine type (i.e. procedure or function) source.
        :return Returns True on success, False otherwise.
        """
        ret = True
        p = re.compile("create\\s+(procedure|function)\\s+([a-zA-Z0-9_]+)")
        matches = p.findall(self._routine_source_code)

        if matches:
            self._routine_type = matches[0][0].lower()

            if self._routine_name != matches[0][1]:
                print("Error: Stored routine name '%s' does not match filename in file '%s'." % (
                    matches[0][1], self._source_filename))
                ret = False
        else:
            ret = False

        if not self._routine_type:
            print("Error: Unable to find the stored routine name and type in file '%s'." % self._source_filename)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _load_routine_file(self):
        """
        Loads the stored routine into the MySQL instance.
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
        self._drop_routine()

        sql = "set sql_mode ='%s'" % self._sql_mode
        StaticDataLayer.execute_none(sql)

        sql = "set names '%s' collate '%s'" % (self._character_set, self._collate)
        StaticDataLayer.execute_none(sql)

        StaticDataLayer.execute_none(routine_source)

    # ------------------------------------------------------------------------------------------------------------------
    def get_bulk_insert_table_columns_info(self):
        """
        Gets the column names and column types of the current table for bulk insert.
        """
        query = """
select 1 from
information_schema.TABLES
where TABLE_SCHEMA = database()
and   TABLE_NAME   = '%s'""" % self._table_name

        table_is_non_temporary = StaticDataLayer.execute_rows(query)

        if len(table_is_non_temporary) == 0:
            query = 'call %s()' % self._routine_name
            StaticDataLayer.execute_sp_none(query)

        query = "describe `%s`" % self._table_name
        columns = StaticDataLayer.execute_rows(query)

        tmp_column_types = []
        tmp_fields = []

        n1 = 0
        for column in columns:
            p = re.compile('(\\w+)')
            c_type = p.findall(column['Type'])
            tmp_column_types.append(c_type[0])
            tmp_fields.append(column['Field'])
            n1 += 1

        n2 = len(self._columns)

        if len(table_is_non_temporary) == 0:
            query = "drop temporary table `%s`" % self._table_name
            StaticDataLayer.execute_none(query)

        if n1 != n2:
            raise Exception("Number of fields %d and number of columns %d don't match." % (n1, n2))

        self._columns_types = tmp_column_types
        self._fields = tmp_fields

    # ------------------------------------------------------------------------------------------------------------------
    def _get_designation_type(self) -> bool:
        """
        Extracts the designation type of the stored routine.
        :return True on success. Otherwise returns False.
        """
        ret = True

        key = self._routine_source_code_lines.index('begin')

        if key != -1:
            p = re.compile('\s*--\s+type:\s*(\w+)\s*(.+)?\s*')
            matches = p.findall(self._routine_source_code_lines[key - 1])

            if matches:
                self._designation_type = matches[0][0]
                tmp = str(matches[0][1])
                if self._designation_type == 'bulk_insert':
                    n = re.compile('([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_,]+)')
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
    def _get_routine_parameters_info(self):
        query = """
select t2.PARAMETER_NAME      parameter_name
,      t2.DATA_TYPE           parameter_type
,      t2.DTD_IDENTIFIER      column_type
,      t2.CHARACTER_SET_NAME  character_set_name
,      t2.COLLATION_NAME      collation
from            information_schema.ROUTINES   t1
left outer join information_schema.PARAMETERS t2  on  t2.SPECIFIC_SCHEMA = t1.ROUTINE_SCHEMA and
                                                      t2.SPECIFIC_NAME   = t1.ROUTINE_NAME and
                                                      t2.PARAMETER_MODE   is not null
where t1.ROUTINE_SCHEMA = database()
and   t1.ROUTINE_NAME   = '%s'""" % self._routine_name

        routine_parameters = StaticDataLayer.execute_rows(query)

        for routine_parameter in routine_parameters:
            if routine_parameter['parameter_name']:
                value = routine_parameter['column_type']
                if 'character_set_name' in routine_parameter:
                    if routine_parameter['character_set_name']:
                        value += ' character set %s' % routine_parameter['character_set_name']
                if 'collation' in routine_parameter:
                    if routine_parameter['character_set_name']:
                        value += ' collation %s' % routine_parameter['collation']

                self._parameters.append({'name': routine_parameter['parameter_name'],
                                         'data_type': routine_parameter['parameter_type'],
                                         'data_type_descriptor': value})

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_routine(self):
        """
        Drops the stored routine if it exists.
        """
        if self._rdbms_old_metadata:
            sql = "drop %s if exists %s" % (self._rdbms_old_metadata['routine_type'], self._routine_name)
            StaticDataLayer.execute_none(sql)


# ----------------------------------------------------------------------------------------------------------------------
