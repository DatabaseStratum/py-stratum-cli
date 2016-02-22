import re
import sys
from pystratum.RoutineLoaderHelper import RoutineLoaderHelper
from pystratum.pgsql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class PgSqlRoutineLoaderHelper(RoutineLoaderHelper):
    """
    Class for loading a single stored routine into a PostgreSQL instance from a (pseudo) SQL file.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _must_reload(self):
        """
        Returns True if the source file must be load or reloaded. Otherwise returns False.
        :return bool:
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
        :return bool: Returns True on success, False otherwise.
        """
        ret = True
        p = re.compile("create\\s+(function)\\s+([a-zA-Z0-9_]+)")
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

        StaticDataLayer.commit()
        StaticDataLayer.execute_none(routine_source)
        StaticDataLayer.commit()

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
    def _get_designation_type(self):
        """
        Extracts the designation type of the stored routine. Returns True on success. Otherwise returns False.

        :rtype bool:
        """
        ret = True

        key = self._routine_source_code_lines.index('begin')

        if key != -1:
            p = re.compile(r'\s*--\s+type:\s*(\w+)\s*(.+)?\s*')
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
    def _get_routine_parameters_info(self):
        query = """
select t2.parameter_name      parameter_name
,      t2.data_type           parameter_type
,      t2.udt_name            column_type
from            information_schema.routines   t1
left outer join information_schema.parameters t2  on  t2.specific_catalog = t1.specific_catalog and
                                                      t2.specific_schema  = t1.specific_schema and
                                                      t2.specific_name    = t1.specific_name and
                                                      t2.parameter_name   is not null
where t1.routine_catalog = current_database()
and   t1.routine_schema  = current_schema()
and   t1.routine_name    = '%s'
order by t2.ordinal_position
""" % self._routine_name

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
            sql = "drop %s if exists %s(%s)" % (self._rdbms_old_metadata['routine_type'],
                                                self._routine_name,
                                                self._rdbms_old_metadata['routine_args'])
            StaticDataLayer.execute_none(sql)


# ----------------------------------------------------------------------------------------------------------------------
