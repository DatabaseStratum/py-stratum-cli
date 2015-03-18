import configparser
import os
import re
from pystratum.Util import Util
from pystratum.mysql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class Constants:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._constants = {}
        """
        All constants.
        :type: dict
        """
        self._old_columns = {}
        """
        The previous column names, widths, and constant names (i.e. the content of $myConstantsFilename upon
        starting this program).
        :type: dict
        """

        self._database = None
        """
        The database name.
        :type: string
        """

        self._host_name = None
        """
        The hostname of the MySQL instance.
        :type: string
        """

        self._password = None
        """
        Password required for logging in on to the MySQL instance.
        :type: string
        """

        self._user_name = None
        """
        User name.
        :type: string
        """

        self._constants_filename = None
        """
        Filename with column names, their widths, and constant names.
        :type: string
        """

        self._prefix = None
        """
        The prefix used for designations a unknown constants.
        :type: string
        """

        self._template_config_filename = None
        """
        Template filename under which the file is generated with the constants.
        :type: string
        """

        self._config_filename = None
        """
        The destination filename with constants.
        :type: string
        """

        self._columns = {}
        """
        All columns in the MySQL schema.
        :type: dict
        """

        self._labels = {}
        """
        All primary key labels, their widths and constant names.
        :type: dict
        """

    # ------------------------------------------------------------------------------------------------------------------
    def main(self, config_filename: str) -> int:
        """
        :param: config_filename string The config filename.
        :return: int
        """
        self._read_configuration_file(config_filename)

        StaticDataLayer.config['user'] = self._user_name
        StaticDataLayer.config['password'] = self._password
        StaticDataLayer.config['database'] = self._database

        StaticDataLayer.connect()

        self.get_old_columns()

        self.get_columns()

        self.enhance_columns()

        self.merge_columns()

        self.write_columns()

        self.get_labels()

        self.fill_constants()

        self.write_target_config_file()

        StaticDataLayer.disconnect()

        return 0

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        :param config_filename string
        """
        config = configparser.ConfigParser()
        config.read(config_filename)

        self._host_name = config.get('database', 'host_name')
        self._user_name = config.get('database', 'user_name')
        self._password = config.get('database', 'password')
        self._database = config.get('database', 'database_name')

        self._constants_filename = config.get('constants', 'columns')
        self._prefix = config.get('constants', 'prefix')
        self._template_config_filename = config.get('constants', 'config_template')
        self._config_filename = config.get('constants', 'config')

    # ------------------------------------------------------------------------------------------------------------------
    def get_old_columns(self):
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
                        p = re.compile('\s*(?:([a-zA-Z0-9_]+)\.)?([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\s+(\d+)\s*(\*|[a-zA-Z0-9_]+)?\s*')
                        matches = p.findall(line)

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
                                self._old_columns[table_name].update({column_name: column_info})
                        else:
                            self._old_columns.update({table_name: {column_name: column_info}})

    # ------------------------------------------------------------------------------------------------------------------
    def get_columns(self):
        """
        Loads the width of all columns in the MySQL schema into columns.
        """
        query = """
(
  select table_name
  ,      column_name
  ,      data_type
  ,      character_maximum_length
  ,      numeric_precision
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
            row['length'] = self.derive_field_length(row)
            if row['table_name'] in self._columns:
                if row['column_name'] in self._columns[row['table_name']]:
                    pass
                else:
                    self._columns[row['table_name']].update({row['column_name']: row})
            else:
                self._columns.update({row['table_name']: {row['column_name']: row}})

    # ------------------------------------------------------------------------------------------------------------------
    def enhance_columns(self):
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
                            self._old_columns[table_name][column_name].update({'constant_name': constant_name})
                        else:
                            constant_name = str(self._old_columns[table_name][column_name]['constant_name']).upper()
                            self._old_columns[table_name][column_name].update({'constant_name': constant_name})

    # ------------------------------------------------------------------------------------------------------------------
    def merge_columns(self):
        """
        Preserves relevant data in old_columns into columns.
        """
        if self._old_columns:
            for table_name, table in sorted(self._old_columns.items()):
                for column_name, column in sorted(table.items()):
                    if 'constant_name' in column:
                        self._columns[table_name][column_name].update({'constant_name': column['constant_name']})

    # ------------------------------------------------------------------------------------------------------------------
    def write_columns(self):
        """
        Writes table and column names, the width of the column, and the constant name (if assigned) to
        constants_filename.
        """
        content = ''
        for table_name, table in sorted(self._columns.items()):
            width1 = 0
            width2 = 0

            for column_name, column in sorted(table.items()):
                width1 = max(len(str(column['column_name'])), width1)
                width2 = max(len(str(column['length'])), width2)

            for column_name, column in sorted(table.items()):
                if column['length'] is not None:
                    if 'constant_name' in column:
                        line_format = "%%s.%%-%ds %%%dd %%s\n" % (int(width1), int(width2))
                        content += line_format % (column['table_name'],
                                                  column['column_name'],
                                                  column['length'],
                                                  column['constant_name'])
                    else:
                        line_format = "%%s.%%-%ds %%%dd\n" % (int(width1), int(width2))
                        content += line_format % (column['table_name'],
                                                  column['column_name'],
                                                  column['length'])

            content += "\n"

        # Save the columns, width and constants to the filesystem.
        Util.write_two_phases(self._constants_filename, content)

    # ------------------------------------------------------------------------------------------------------------------
    def get_labels(self):
        """
        Gets all primary key labels from the MySQL database.
        """
        query_string = """
select t1.table_name  `table_name`
,      t1.column_name `id`
,      t2.column_name `label`
from       information_schema.columns t1
inner join information_schema.columns t2 on t1.table_name = t2.table_name
where t1.table_schema = database()
and   t1.extra        = 'auto_increment'
and   t2.table_schema = database()
and   t2.column_name like '%%\\_label'"""

        tables = StaticDataLayer.execute_rows(query_string)
        for table in tables:
            query_string = """
select `%s`  as `id`
,      `%s`  as `label`
from   `%s`
where   nullif(`%s`,'') is not null""" % (table['id'],
                                          table['label'],
                                          table['table_name'],
                                          table['label'])

            rows = StaticDataLayer.execute_rows(query_string)
            for row in rows:
                self._labels.update({row['label']: row['id']})

    # ------------------------------------------------------------------------------------------------------------------
    def fill_constants(self):
        """
        Merges columns and labels (i.e. all known constants) into constants.
        """
        for table_name, table in sorted(self._columns.items()):
            for column_name, column in sorted(table.items()):
                if 'constant_name' in column:
                    self._constants.update({column['constant_name']: column['length']})

        for label, label_id in sorted(self._labels.items()):
            self._constants.update({label: label_id})

    # ------------------------------------------------------------------------------------------------------------------
    def write_target_config_file(self):
        """
        Creates a python configuration file with constants.
        :return:
        """
        content = ''
        for constant, value in sorted(self._constants.items()):
            content += "%s = %s\n" % (str(constant), str(value))

            # Save the configuration file.
        Util.write_two_phases(self._config_filename, content)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def derive_field_length(the_column: dict) -> int:
        """
        Returns the width of a field based on column.
        :param the_column dict The column of which the field is based.
        :returns int The width of the column.
        """
        types_length = {'tinyint': the_column['numeric_precision'],
                        'smallint': the_column['numeric_precision'],
                        'mediumint': the_column['numeric_precision'],
                        'int': the_column['numeric_precision'],
                        'bigint': the_column['numeric_precision'],
                        'decimal': the_column['numeric_precision'],
                        'float': the_column['numeric_precision'],
                        'double': the_column['numeric_precision'],
                        'char': the_column['character_maximum_length'],
                        'varchar': the_column['character_maximum_length'],
                        'binary': the_column['character_maximum_length'],
                        'varbinary': the_column['character_maximum_length'],
                        'tinytext': the_column['character_maximum_length'],
                        'text': the_column['character_maximum_length'],
                        'mediumtext': the_column['character_maximum_length'],
                        'longtext': the_column['character_maximum_length'],
                        'tinyblob': the_column['character_maximum_length'],
                        'blob': the_column['character_maximum_length'],
                        'mediumblob': the_column['character_maximum_length'],
                        'longblob': the_column['character_maximum_length'],
                        'bit': the_column['character_maximum_length'],
                        'timestamp': 16,
                        'year': 4,
                        'time': 8,
                        'date': 10,
                        'datetime': 16,
                        'enum': None,
                        'set': None}

        if the_column['data_type'] in types_length:
            return types_length[the_column['data_type']]
        else:
            # assert failed
            print("Unknown type '%s'." % the_column['data_type'])
            return None

# ----------------------------------------------------------------------------------------------------------------------
