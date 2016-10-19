"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import re

from mysql import connector

from pystratum.RoutineLoaderHelper import RoutineLoaderHelper
from pystratum_mysql.MySqlMetadataDataLayer import MySqlMetadataDataLayer
from pystratum_mysql.helper.MySqlDataTypeHelper import MySqlDataTypeHelper


class MySqlRoutineLoaderHelper(RoutineLoaderHelper):
    """
    Class for loading a single stored routine into a MySQL instance from a (pseudo) SQL file.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 routine_filename,
                 routine_file_encoding,
                 pystratum_old_metadata,
                 replace_pairs,
                 rdbms_old_metadata,
                 sql_mode,
                 character_set,
                 collate,
                 io):
        """
        Object constructor.

        :param str routine_filename: The filename of the source of the stored routine.
        :param str routine_file_encoding: The encoding of the source file.
        :param dict pystratum_old_metadata: The metadata of the stored routine from PyStratum.
        :param dict[str,str] replace_pairs: A map from placeholders to their actual values.
        :param dict rdbms_old_metadata: The old metadata of the stored routine from MS SQL Server.
        :param str sql_mode: The SQL mode under which the stored routine must be loaded and run.
        :param str character_set: The default character set under which the stored routine must be loaded and run.
        :param str collate: The default collate under which the stored routine must be loaded and run.
        :param pystratum.style.PyStratumStyle.PyStratumStyle io: The output decorator.
        """

        RoutineLoaderHelper.__init__(self,
                                     routine_filename,
                                     routine_file_encoding,
                                     pystratum_old_metadata,
                                     replace_pairs,
                                     rdbms_old_metadata,
                                     io)

        self._sql_mode = sql_mode
        """
        The SQL-mode under which the stored routine will be loaded and run.

        :type: str
        """

        self._character_set = character_set
        """
        The default character set under which the stored routine will be loaded and run.

        :type: str
        """

        self._collate = collate
        """
        The default collate under which the stored routine will be loaded and run.

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

        if self._rdbms_old_metadata['sql_mode'] != self._sql_mode:
            return True

        if self._rdbms_old_metadata['character_set_client'] != self._character_set:
            return True

        if self._rdbms_old_metadata['collation_connection'] != self._collate:
            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def _get_name(self):
        """
        Extracts the name of the stored routine and the stored routine type (i.e. procedure or function) source.
        Returns True on success, False otherwise.

        :rtype: bool
        """
        ret = True
        prog = re.compile("create\\s+(procedure|function)\\s+([a-zA-Z0-9_]+)")
        matches = prog.findall(self._routine_source_code)

        if matches:
            self._routine_type = matches[0][0].lower()

            if self._routine_name != matches[0][1]:
                self._io.error('Stored routine name {0} does not match filename in file {1}'.
                               format(matches[0][1], self._source_filename))
                ret = False
        else:
            ret = False

        if not self._routine_type:
            self._io.error('Unable to find the stored routine name and type in file {0}'.
                           format(self._source_filename))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _get_data_type_helper(self):
        """
        Returns a data type helper object for MySQL.

        :rtype: pystratum.helper.DataTypeHelper.DataTypeHelper
        """
        return MySqlDataTypeHelper()

    # ------------------------------------------------------------------------------------------------------------------
    def _is_start_or_store_routine(self, line):
        """
        Returns True if a line is the start of the code of the stored routine.

        :param str line: The line with source code of the stored routine.

        :rtype: bool
        """
        return re.match(r'^\s*create\s+(procedure|function)', line) is not None

    # ------------------------------------------------------------------------------------------------------------------
    def _load_routine_file(self):
        """
        Loads the stored routine into the MySQL instance.
        """
        self._io.text('Loading {0} <dbo>{1}</dbo>'.format(self._routine_type, self._routine_name))

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

        MySqlMetadataDataLayer.set_sql_mode(self._sql_mode)

        MySqlMetadataDataLayer.set_character_set(self._character_set, self._collate)

        MySqlMetadataDataLayer.execute_none(routine_source)

    # ------------------------------------------------------------------------------------------------------------------
    def _log_exception(self, exception):
        """
        Logs an exception.

        :param Exception exception: The exception.
        """
        RoutineLoaderHelper._log_exception(self, exception)

        if isinstance(exception, connector.errors.Error):
            if exception.errno == 1064:
                # Exception is caused by an invalid SQL statement.
                sql = MySqlMetadataDataLayer.last_sql()
                if sql:
                    sql = sql.strip()
                    # The format of a 1064 message is: %s near '%s' at line %d
                    parts = re.search(r'(\d+)$', exception.msg)
                    if parts:
                        error_line = int(parts.group(1))
                    else:
                        error_line = 0

                    self._print_sql_with_error(sql, error_line)

    # ------------------------------------------------------------------------------------------------------------------
    def get_bulk_insert_table_columns_info(self):
        """
        Gets the column names and column types of the current table for bulk insert.
        """
        table_is_non_temporary = MySqlMetadataDataLayer.check_table_exists(self._table_name)

        if not table_is_non_temporary:
            MySqlMetadataDataLayer.call_stored_routine(self._routine_name)

        columns = MySqlMetadataDataLayer.describe_table(self._table_name)

        tmp_column_types = []
        tmp_fields = []

        n1 = 0
        for column in columns:
            prog = re.compile('(\\w+)')
            c_type = prog.findall(column['Type'])
            tmp_column_types.append(c_type[0])
            tmp_fields.append(column['Field'])
            n1 += 1

        n2 = len(self._columns)

        if not table_is_non_temporary:
            MySqlMetadataDataLayer.drop_temporary_table(self._table_name)

        if n1 != n2:
            raise Exception("Number of fields %d and number of columns %d don't match." % (n1, n2))

        self._columns_types = tmp_column_types
        self._fields = tmp_fields

    # ------------------------------------------------------------------------------------------------------------------
    def _get_designation_type(self):
        """
        Extracts the designation type of the stored routine. Returns True on success. Otherwise returns False.

        :rtype: bool
        """
        ret = True

        positions = self._get_create_begin_block_positions()
        if positions[0] != -1:
            prog = re.compile(r'\s*--\s+type:\s*(\w+)\s*(.+)?\s*')
            for x in range(positions[0], positions[1]):
                matches = prog.findall(self._routine_source_code_lines[x])
                if matches:
                    self._designation_type = matches[0][0]
                    tmp = str(matches[0][1])
                    if self._designation_type == 'bulk_insert':
                        n = re.compile(r'([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_,]+)')
                        info = n.findall(tmp)

                        if not info:
                            self._io.error('Expected: -- type: bulk_insert <table_name> <columns> in file {0}'.
                                           format(self._source_filename))
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
            self._io.error("Unable to find the designation type of the stored routine in file {0}".
                           format(self._source_filename))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _get_create_begin_block_positions(self):
        """
        Return start row based on 'create procedure' and end row based on 'begin'

        :rtype: tuple
        """
        start = 0
        end = self._routine_source_code_lines.index('begin')
        for (i, item) in enumerate(self._routine_source_code_lines):
            if 'create procedure' in item:
                start = i + 1

        return start, end

    # ------------------------------------------------------------------------------------------------------------------
    def _get_routine_parameters_info(self):
        """
        Retrieves information about the stored routine parameters from the meta data of MySQL.
        """
        routine_parameters = MySqlMetadataDataLayer.get_routine_parameters(self._routine_name)
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
                                         'numeric_precision': routine_parameter['numeric_precision'],
                                         'numeric_scale': routine_parameter['numeric_scale'],
                                         'data_type_descriptor': value})

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_routine(self):
        """
        Drops the stored routine if it exists.
        """
        if self._rdbms_old_metadata:
            MySqlMetadataDataLayer.drop_stored_routine(self._rdbms_old_metadata['routine_type'], self._routine_name)

# ----------------------------------------------------------------------------------------------------------------------
