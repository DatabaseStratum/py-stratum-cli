import os
import re

from pystratum.Util import Util
from pystratum.mssql.MsSqlConnection import MsSqlConnection
from pystratum.mssql.StaticDataLayer import StaticDataLayer
from pystratum.Constants import Constants


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlConstants(MsSqlConnection, Constants):
    """
    Class for creating constants based on column widths, and auto increment columns and labels for MS SQL Server
    databases.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        Constants.__init__(self)
        MsSqlConnection.__init__(self)

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
                        p = re.compile('\s*(?:([a-zA-Z0-9_]+)\.)?([a-zA-Z0-9_]+)\.'
                                       '([a-zA-Z0-9_]+)\s+(\d+)\s*(\*|[a-zA-Z0-9_]+)?\s*')
                        matches = p.findall(line)

                        if matches:
                            matches = matches[0]
                            schema_name = str(matches[0])
                            table_name = str(matches[1])
                            column_name = str(matches[2])
                            length = str(matches[3])
                            constant_name = str(matches[4])

                            if constant_name:
                                column_info = {'schema_name': schema_name,
                                               'table_name': table_name,
                                               'column_name': column_name,
                                               'length': length,
                                               'constant_name': constant_name}
                            else:
                                column_info = {'schema_name': schema_name,
                                               'table_name': table_name,
                                               'column_name': column_name,
                                               'length': length}

                            if schema_name in self._old_columns:
                                if table_name in self._old_columns[schema_name]:
                                    if column_name in self._old_columns[schema_name][table_name]:
                                        pass
                                    else:
                                        self._old_columns[schema_name][table_name][column_name] = column_info
                                else:
                                    self._old_columns[schema_name][table_name] = {column_name: column_info}
                            else:
                                self._old_columns[schema_name] = {table_name: {column_name: column_info}}

    # ------------------------------------------------------------------------------------------------------------------
    def _get_columns(self):
        """
        Retrieves metadata all columns in the MySQL schema.
        """
        query = """
select scm.name                   schema_name
,      tab.name                   table_name
,      col.name                   column_name
,      isnull(stp.name,utp.name)  data_type
,      col.max_length
,      col.precision
,      col.scale
,      col.column_id
from            sys.columns col
inner join      sys.types   utp  on  utp.user_type_id = col.user_type_id and
                                     utp.system_type_id = col.system_type_id
left outer join sys.types   stp  on  utp.is_user_defined = 1 and
                                     stp.is_user_defined = 0 and
                                     utp.system_type_id = stp.system_type_id and
                                     utp.user_type_id <> stp.user_type_id  and
                                     stp.user_type_id = stp.system_type_id
inner join      sys.tables  tab  on  col.object_id = tab.object_id
inner join      sys.schemas scm  on  tab.schema_id = scm.schema_id
where tab.type in ('U','S','V')
order by  scm.name
,         tab.name
,         col.column_id"""

        rows = StaticDataLayer.execute_rows(query)

        for row in rows:
            row['length'] = MsSqlConstants.derive_field_length(row)

            if row['schema_name'] in self._columns:
                if row['table_name'] in self._columns[row['schema_name']]:
                    if row['column_name'] in self._columns[row['schema_name']][row['table_name']]:
                        pass
                    else:
                        self._columns[row['schema_name']][row['table_name']][row['column_name']] = row
                else:
                    self._columns[row['schema_name']][row['table_name']] = {row['column_name']: row}
            else:
                self._columns[row['schema_name']] = {row['table_name']: {row['column_name']: row}}

    # ------------------------------------------------------------------------------------------------------------------
    def _enhance_columns(self):
        """
        Enhances old_columns as follows:
        If the constant name is *, is is replaced with the column name prefixed by prefix in uppercase.
        Otherwise the constant name is set to uppercase.
        """
        if self._old_columns:
            for schema_name, schema in sorted(self._old_columns.items()):
                for table_name, table in sorted(schema.items()):
                    for column_name, column in sorted(table.items()):
                        if 'constant_name' in column:
                            if column['constant_name'].strip() == '*':
                                constant_name = str(self._prefix + column['column_name']).upper()
                                self._old_columns[schema_name][table_name][column_name]['constant_name'] = constant_name
                            else:
                                constant_name = str(
                                    self._old_columns[schema_name][table_name][column_name]['constant_name']).upper()
                                self._old_columns[schema_name][table_name][column_name]['constant_name'] = constant_name

    # ------------------------------------------------------------------------------------------------------------------
    def _merge_columns(self):
        """
        Preserves relevant data in old_columns into columns.
        """
        if self._old_columns:
            for schema_name, schema in sorted(self._old_columns.items()):
                for table_name, table in sorted(schema.items()):
                    for column_name, column in sorted(table.items()):
                        if 'constant_name' in column:
                            try:
                                self._columns[schema_name][table_name][column_name]['constant_name'] = \
                                    column['constant_name']
                            except KeyError:
                                # Either the column, table, or whole schema is not present anymore.
                                pass

    # ------------------------------------------------------------------------------------------------------------------
    def _write_columns(self):
        """
        Writes table and column names, the width of the column, and the constant name (if assigned) to
        constants_filename.
        """
        content = ''

        for schema_name, schema in sorted(self._columns.items()):
            for table_name, table in sorted(schema.items()):
                width1 = 0
                width2 = 0

                key_map = {}
                for column_name, column in table.items():
                    key_map[column['column_id']] = column_name
                    width1 = max(len(str(column['column_name'])), width1)
                    width2 = max(len(str(column['length'])), width2)

                for col_id, column_name in sorted(key_map.items()):
                    if table[column_name]['length'] is not None:
                        if 'constant_name' in table[column_name]:
                            line_format = "%%s.%%s.%%-%ds %%%dd %%s\n" % (int(width1), int(width2))
                            content += line_format % (schema_name,
                                                      table[column_name]['table_name'],
                                                      table[column_name]['column_name'],
                                                      table[column_name]['length'],
                                                      table[column_name]['constant_name'])
                        else:
                            line_format = "%%s.%%s.%%-%ds %%%dd\n" % (int(width1), int(width2))
                            content += line_format % (schema_name,
                                                      table[column_name]['table_name'],
                                                      table[column_name]['column_name'],
                                                      table[column_name]['length'])

                content += "\n"""

        # Save the columns, width, and constants to the filesystem.
        Util.write_two_phases(self._constants_filename, content)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_labels(self):
        """
        Gets all primary key labels from the MySQL database.
        """
        query_string = """
select scm.name  schema_name
,      tab.name  table_name
,      cl1.name  label
,      cl2.name  id
from       sys.schemas     scm
inner join sys.tables      tab  on  tab.[schema_id] = scm.[schema_id]
inner join sys.all_columns cl1  on  cl1.[object_id] = tab.[object_id]
inner join sys.all_columns cl2  on  cl2.[object_id] = tab.[object_id]
where cl1.name like '%_label'
and   cl2.name like '%_id'
and   cl2.is_identity = 1"""

        tables = StaticDataLayer.execute_rows(query_string)

        for table in tables:
            query_string = """
select tab.[%s] id
,      tab.[%s] label
from   [%s].[%s].[%s] tab
where  nullif(tab.[%s],'') is not null""" \
                           % (table['id'],
                              table['label'],
                              self._database,
                              table['schema_name'],
                              table['table_name'],
                              table['label'])

            rows = StaticDataLayer.execute_rows(query_string)
            for row in rows:
                if row['label'] not in self._labels:
                    self._labels[row['label']] = row['id']
                else:
                    # todo improve exception.
                    Exception("Duplicate label '%s'")

    # ------------------------------------------------------------------------------------------------------------------
    def _fill_constants(self):
        """
        Merges columns and labels (i.e. all known constants) into constants.
        """
        for schema_name, schema in sorted(self._columns.items()):
            for table_name, table in sorted(schema.items()):
                for column_name, column in sorted(table.items()):
                    if 'constant_name' in column:
                        self._constants[column['constant_name']] = column['length']

        for label, label_id in sorted(self._labels.items()):
            self._constants[label] = label_id

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def derive_field_length(column: dict) -> int:
        """
        Returns the width of a field based on column.
        :param column dict The column of which the field is based.
        :returns int The width of the column.
        """
        data_type = column['data_type']

        if data_type == 'bigint':
            return column['precision']

        if data_type == 'int':
            return column['precision']

        if data_type == 'smallint':
            return column['precision']

        if data_type == 'tinyint':
            return column['precision']

        if data_type == 'bit':
            return column['max_length']

        if data_type == 'money':
            return column['precision']

        if data_type == 'smallmoney':
            return column['precision']

        if data_type == 'decimal':
            return column['precision']

        if data_type == 'numeric':
            return column['precision']

        if data_type == 'float':
            return column['precision']

        if data_type == 'real':
            return column['precision']

        if data_type == 'date':
            return column['precision']

        if data_type == 'datetime':
            return column['precision']

        if data_type == 'datetime2':
            return column['precision']

        if data_type == 'datetimeoffset':
            return column['precision']

        if data_type == 'smalldatetime':
            return column['precision']

        if data_type == 'time':
            return column['precision']

        if data_type == 'char':
            return column['max_length']

        if data_type == 'varchar':
            if column['max_length'] == -1:
                # This is a varchar(max) data type.
                return 2147483647

            return column['max_length']

        if data_type == 'text':
            return 2147483647

        if data_type == 'nchar':
            return column['max_length'] / 2

        if data_type == 'nvarchar':
            if column['max_length'] == -1:
                # This is a nvarchar(max) data type.
                return 1073741823

            return column['max_length'] / 2

        if data_type == 'ntext':
            return 1073741823

        if data_type == 'binary':
            return column['max_length']

        if data_type == 'varbinary':
            return column['max_length']

        if data_type == 'image':
            return 2147483647

        if data_type == 'xml':
            return 2147483647

        if data_type == 'geography':
            if column['max_length'] == -1:
                # This is a varchar(max) data type.
                return 2147483647

        if data_type == 'geometry':
            if column['max_length'] == -1:
                # This is a varchar(max) data type.
                return 2147483647

        raise Exception("Unexpected data type '%s'." % data_type)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        :param config_filename
        """
        Constants._read_configuration_file(self, config_filename)
        MsSqlConnection._read_configuration_file(self, config_filename)


# ----------------------------------------------------------------------------------------------------------------------

