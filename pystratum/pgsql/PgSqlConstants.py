import os
import re

from pystratum.Util import Util
from pystratum.pgsql.PgSqlConnection import PgSqlConnection
from pystratum.pgsql.StaticDataLayer import StaticDataLayer
from pystratum.Constants import Constants


# ----------------------------------------------------------------------------------------------------------------------
class PgSqlConstants(PgSqlConnection, Constants):
    """
    Class for creating constants based on column widths, and auto increment columns and labels for PostgreSQL databases.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        Constants.__init__(self)
        PgSqlConnection.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_old_columns(self):
        """
        Reads from file constants_filename the previous table and column names, the width of the column,
        and the constant name (if assigned) and stores this data in old_columns.
        """
        if os.path.exists(self._constants_filename):
            with open(self._constants_filename, 'r') as f:
                line_number = 0
                for line in f:
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
                                column_info = {'table_name': table_name,
                                               'column_name': column_name,
                                               'length': length,
                                               'constant_name': constant_name}
                            else:
                                column_info = {'table_name': table_name,
                                               'column_name': column_name,
                                               'length': length}

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
  where  table_catalog = current_database()
  and    table_schema  = current_schema()
  and    table_name  similar to '[a-zA-Z0-9_]*'
  and    column_name similar to '[a-zA-Z0-9_]*'
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
  where  1=0 and table_catalog = current_database()
  and    table_name  similar to '[a-zA-Z0-9_]*'
  and    column_name similar to '[a-zA-Z0-9_]*'
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
select t1.table_name  "table_name"
,      t1.column_name "id"
,      t2.column_name "label"
from       information_schema.columns t1
inner join information_schema.columns t2 on t1.table_name = t2.table_name
where t1.table_catalog = current_database()
and   t1.table_schema = current_schema()
and   t1.column_default like 'nextval(%%)'
and   t2.table_catalog = current_database()
and   t2.table_schema  = current_schema()
and   t2.column_name like '%%_label'
"""

        tables = StaticDataLayer.execute_rows(query_string)

        for table in tables:
            query_string = """
select \"{0!s}\"  as id
,      \"{1!s}\"  as label
from   \"{2!s}\"
where   nullif(\"{3!s}\",'') is not null""".format(table['id'],
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
    def derive_field_length(column):
        """
        Returns the width of a field based on the data type of column.

        :param dict column: The column of which the field is based.

        :rtype int:
        """
        types_length = {'bigint': 21,
                        'integer': 11,
                        'smallint': 6,
                        'bit': column['character_maximum_length'],
                        'money': None,  # @todo max-length
                        'boolean': None,  # @todo max-length
                        'double': column['numeric_precision'],
                        'numeric': column['numeric_precision'],
                        'real': None,  # @todo max-length
                        'character': column['character_maximum_length'],
                        'character varying': column['character_maximum_length'],
                        'point': None,  # @todo max-length
                        'polygon': None,  # @todo max-length
                        'text': None,  # @todo max-length
                        'bytea': None,  # @todo max-length
                        'xml': None,  # @todo max-length
                        'USER-DEFINED': None,
                        'timestamp without time zone': 16,
                        'time without time zone': 8,
                        'date': 10}

        if column['data_type'] in types_length:
            return types_length[column['data_type']]

        raise Exception("Unexpected type '{0!s}'.".format(column['data_type']))

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename):
        """
        Reads parameters from the configuration file.

        :param str config_filename:
        """
        Constants._read_configuration_file(self, config_filename)
        PgSqlConnection._read_configuration_file(self, config_filename)

# ----------------------------------------------------------------------------------------------------------------------
