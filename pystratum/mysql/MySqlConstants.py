import os
import re

from pystratum.Util import Util
from pystratum.mysql.MySqlConnection import MySqlConnection
from pystratum.mysql.StaticDataLayer import StaticDataLayer
from pystratum.Constants import Constants


# ----------------------------------------------------------------------------------------------------------------------
class MySqlConstants(MySqlConnection, Constants):
    """
    Class for creating constants based on column widths, and auto increment columns and labels for MySQL databases.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        Constants.__init__(self)
        MySqlConnection.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_old_columns(self):
        """
        Reads from file constants_filename the previous table and column names, the width of the column,
        and the constant name (if assigned) and stores this data in old_columns.
        """
        if os.path.exists(self._constants_filename):
            with open(self._constants_filename, 'r') as file:
                line_number = 0
                for line in file:
                    line_number += 1
                    if line != "\n":
                        p = re.compile(r'\s*(?:([a-zA-Z0-9_]+)\.)?([a-zA-Z0-9_]+)\.'
                                       r'([a-zA-Z0-9_]+)\s+(\d+)\s*(\*|[a-zA-Z0-9_]+)?\s*')
                        matches = p.findall(line)

                        if matches:
                            matches = matches[0]
                            schema_name = str(matches[0])
                            table_name = str(matches[1])
                            column_name = str(matches[2])
                            length = str(matches[3])
                            constant_name = str(matches[4])

                            if schema_name:
                                table_name = schema_name + '.' + table_name

                            if constant_name:
                                column_info = {'table_name':    table_name,
                                               'column_name':   column_name,
                                               'length':        length,
                                               'constant_name': constant_name}
                            else:
                                column_info = {'table_name':  table_name,
                                               'column_name': column_name,
                                               'length':      length}

                            if table_name in self._old_columns:
                                if column_name in self._old_columns[table_name]:
                                    pass
                                else:
                                    self._old_columns[table_name][column_name] = column_info
                            else:
                                self._old_columns[table_name] = {column_name: column_info}

    # ------------------------------------------------------------------------------------------------------------------
    def _get_columns(self):
        """
        Retrieves metadata all columns in the MySQL schema.
        """
        query = """
(
  select table_name
  ,      column_name
  ,      data_type
  ,      character_maximum_length
  ,      numeric_precision
  ,      ordinal_position
  from   information_schema.COLUMNS
  where  table_schema = database()
  and    table_name  rlike '^[a-zA-Z0-9_]*$'
  and    column_name rlike '^[a-zA-Z0-9_]*$'
  order by table_name
  ,        ordinal_position
)

union all

(
  select concat(table_schema,'.',table_name) table_name
  ,      column_name
  ,      data_type
  ,      character_maximum_length
  ,      numeric_precision
  ,      ordinal_position
  from   information_schema.COLUMNS
  where  table_name  rlike '^[a-zA-Z0-9_]*$'
  and    column_name rlike '^[a-zA-Z0-9_]*$'
  order by table_schema
  ,        table_name
  ,        ordinal_position
)
"""

        rows = StaticDataLayer.execute_rows(query)

        for row in rows:
            # Enhance row with the actual length of the column.
            row['length'] = self.derive_field_length(row)

            if row['table_name'] in self._columns:
                if row['column_name'] in self._columns[row['table_name']]:
                    pass
                else:
                    self._columns[row['table_name']][row['column_name']] = row
            else:
                self._columns[row['table_name']] = {row['column_name']: row}

    # ------------------------------------------------------------------------------------------------------------------
    def _enhance_columns(self):
        """
        Enhances old_columns as follows:
        If the constant name is *, is is replaced with the column name prefixed by prefix in uppercase.
        Otherwise the constant name is set to uppercase.
        """
        if self._old_columns:
            for table_name, table in sorted(self._old_columns.items()):
                for column_name, column in sorted(table.items()):
                    table_name = column['table_name']
                    column_name = column['column_name']

                    if 'constant_name' in column:
                        if column['constant_name'].strip() == '*':
                            constant_name = str(self._prefix + column['column_name']).upper()
                            self._old_columns[table_name][column_name]['constant_name'] = constant_name
                        else:
                            constant_name = str(self._old_columns[table_name][column_name]['constant_name']).upper()
                            self._old_columns[table_name][column_name]['constant_name'] = constant_name

    # ------------------------------------------------------------------------------------------------------------------
    def _merge_columns(self):
        """
        Preserves relevant data in old_columns into columns.
        """
        if self._old_columns:
            for table_name, table in sorted(self._old_columns.items()):
                for column_name, column in sorted(table.items()):
                    if 'constant_name' in column:
                        try:
                            self._columns[table_name][column_name]['constant_name'] = column['constant_name']
                        except KeyError:
                            # Either the column or table is not present anymore.
                            print('Dropping constant {1} because column is not present anymore'.
                                  format(column['constant_name']))

    # ------------------------------------------------------------------------------------------------------------------
    def _write_columns(self):
        """
        Writes table and column names, the width of the column, and the constant name (if assigned) to
        constants_filename.
        """
        content = ''
        for table_name, table in sorted(self._columns.items()):
            width1 = 0
            width2 = 0

            key_map = {}
            for column_name, column in table.items():
                key_map[column['ordinal_position']] = column_name
                width1 = max(len(str(column['column_name'])), width1)
                width2 = max(len(str(column['length'])), width2)

            for ord_position, column_name in sorted(key_map.items()):
                if table[column_name]['length'] is not None:
                    if 'constant_name' in table[column_name]:
                        line_format = "%s.%-{0:d}s %{1:d}d %s\n".format(int(width1), int(width2))
                        content += line_format % (table[column_name]['table_name'],
                                                  table[column_name]['column_name'],
                                                  table[column_name]['length'],
                                                  table[column_name]['constant_name'])
                    else:
                        line_format = "%s.%-{0:d}s %{1:d}d\n".format(int(width1), int(width2))
                        content += line_format % (table[column_name]['table_name'],
                                                  table[column_name]['column_name'],
                                                  table[column_name]['length'])

            content += "\n"

        # Save the columns, width and constants to the filesystem.
        Util.write_two_phases(self._constants_filename, content)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_labels(self):
        """
        Gets all primary key labels from the MySQL database.
        """
        query_string = """
select t1.TABLE_NAME  table_name
,      t1.COLUMN_NAME id
,      t2.COLUMN_NAME label
from       information_schema.COLUMNS t1
inner join information_schema.COLUMNS t2 on t1.TABLE_NAME = t2.TABLE_NAME
where t1.TABLE_SCHEMA = database()
and   t1.EXTRA        = 'auto_increment'
and   t2.TABLE_SCHEMA = database()
and   t2.COLUMN_NAME like '%%\\_label'"""

        tables = StaticDataLayer.execute_rows(query_string)

        for table in tables:
            query_string = """
select `{0!s}`  as `id`
,      `{1!s}`  as `label`
from   `{2!s}`
where   nullif(`{3!s}`,'') is not null""".format(table['id'],
                                                 table['label'],
                                                 table['table_name'],
                                                 table['label'])

            rows = StaticDataLayer.execute_rows(query_string)
            for row in rows:
                self._labels[row['label']] = row['id']

    # ------------------------------------------------------------------------------------------------------------------
    def _fill_constants(self):
        """
        Merges columns and labels (i.e. all known constants) into constants.
        """
        for table_name, table in sorted(self._columns.items()):
            for column_name, column in sorted(table.items()):
                if 'constant_name' in column:
                    self._constants[column['constant_name']] = column['length']

        for label, label_id in sorted(self._labels.items()):
            self._constants[label] = label_id

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def derive_field_length(the_column: dict) -> int:
        """
        Returns the width of a field based on column.
        :param the_column dict The column of which the field is based.
        :returns The width of the column.
        """
        types_length = {'tinyint': the_column   ['numeric_precision'],
                        'smallint': the_column  ['numeric_precision'],
                        'mediumint': the_column ['numeric_precision'],
                        'int': the_column       ['numeric_precision'],
                        'bigint': the_column    ['numeric_precision'],
                        'decimal': the_column   ['numeric_precision'],
                        'float': the_column     ['numeric_precision'],
                        'double': the_column    ['numeric_precision'],
                        'char': the_column      ['character_maximum_length'],
                        'varchar': the_column   ['character_maximum_length'],
                        'binary': the_column    ['character_maximum_length'],
                        'varbinary': the_column ['character_maximum_length'],
                        'tinytext': the_column  ['character_maximum_length'],
                        'text': the_column      ['character_maximum_length'],
                        'mediumtext': the_column['character_maximum_length'],
                        'longtext': the_column  ['character_maximum_length'],
                        'tinyblob': the_column  ['character_maximum_length'],
                        'blob': the_column      ['character_maximum_length'],
                        'mediumblob': the_column['character_maximum_length'],
                        'longblob': the_column  ['character_maximum_length'],
                        'bit': the_column       ['character_maximum_length'],
                        'timestamp':            16,
                        'year':                 4,
                        'time':                 8,
                        'date':                 10,
                        'datetime':             16,
                        'enum':                 None,
                        'set':                  None}

        if the_column['data_type'] in types_length:
            return types_length[the_column['data_type']]

        raise Exception("Unexpected type '{0!s}'.".format(the_column['data_type']))

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        :param config_filename
        """
        Constants._read_configuration_file(self, config_filename)
        MySqlConnection._read_configuration_file(self, config_filename)

# ----------------------------------------------------------------------------------------------------------------------
