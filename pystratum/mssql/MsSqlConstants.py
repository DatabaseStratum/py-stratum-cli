import os
import re

from pystratum.Util import Util
from pystratum.mssql.StaticDataLayer import StaticDataLayer
from pystratum.Constants import Constants


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlConstants(Constants):
    """
    Class for creating constants based on column widths, and auto increment columns and labels for MS SQL Server
    databases.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def connect(self):
        StaticDataLayer.connect(self._host_name,
                                self._user_name,
                                self._password,
                                self._database)

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self):
        StaticDataLayer.disconnect()

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
                        p = re.compile('\s*(?:([a-zA-Z0-9_]+)\.)?([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\s+(\d+)\s*(\*|[a-zA-Z0-9_]+)?\s*')
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
                                        self._old_columns[schema_name][table_name].update({column_name: column_info})
                                else:
                                    self._old_columns[schema_name].update({table_name: {column_name: column_info}})
                            else:
                                self._old_columns.update({schema_name: {table_name: {column_name: column_info}}})

    # ------------------------------------------------------------------------------------------------------------------
    def _get_columns(self):
        """
        Retrieves metadata all columns in the MySQL schema.
        """
        query = """
select scm.name  schema_name
,      tab.name  table_name
,      col.name  column_name
,      typ.name  data_type
,      col.max_length length
,      col.precision
,      col.scale
from       sys.schemas     scm
inner join sys.tables      tab  on  tab.[schema_id] = scm.[schema_id]
inner join sys.all_columns col  on  col.[object_id] = tab.[object_id]
inner join sys.types       typ  on  typ.user_type_id = col.system_type_id
where tab.type in ('U','S','V')
order by  scm.name
,         tab.name
,         col.column_id
;"""

        rows = StaticDataLayer.execute_rows(query)

        for row in rows:
            if row['schema_name'] in self._columns:
                if row['table_name'] in self._columns[row['schema_name']]:
                    if row['column_name'] in self._columns[row['schema_name']][row['table_name']]:
                        pass
                    else:
                        self._columns[row['schema_name']][row['table_name']].update({row['column_name']: row})
                else:
                    self._columns[row['schema_name']].update({row['table_name']: {row['column_name']: row}})
            else:
                self._columns.update({row['schema_name']: {row['table_name']: {row['column_name']: row}}})

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
                                self._old_columns[schema_name][table_name][column_name].update({'constant_name': constant_name})
                            else:
                                constant_name = str(self._old_columns[schema_name][table_name][column_name]['constant_name']).upper()
                                self._old_columns[schema_name][table_name][column_name].update({'constant_name': constant_name})

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
                            self._columns[schema_name][table_name][column_name].update({'constant_name': column['constant_name']})

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

                for column_name, column in sorted(table.items()):
                    width1 = max(len(str(column['column_name'])), width1)
                    width2 = max(len(str(column['length'])), width2)

                for column_name, column in sorted(table.items()):
                    if column['length'] is not None:
                        if 'constant_name' in column:
                            line_format = "%%s.%%s.%%-%ds %%%dd %%s\n" % (int(width1), int(width2))
                            content += line_format % (schema_name,
                                                      column['table_name'],
                                                      column['column_name'],
                                                      column['length'],
                                                      column['constant_name'])
                        else:
                            line_format = "%%s.%%s.%%-%ds %%%dd\n" % (int(width1), int(width2))
                            content += line_format % (schema_name,
                                                      column['table_name'],
                                                      column['column_name'],
                                                      column['length'])

                content += "\n"

        # Save the columns, width and constants to the filesystem.
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
and   cl2.is_identity = 1
;"""

        tables = StaticDataLayer.execute_rows(query_string)

        for table in tables:
            query_string = """
select tab.%s id
,      tab.%s label
from   %s.%s.%s tab
where  nullif(tab.%s,'') is not null
;""" % (table['id'],
        table['label'],
        self._database,
        table['schema_name'],
        table['table_name'],
        table['label'])

            rows = StaticDataLayer.execute_rows(query_string)

            for row in rows:
                if row['label'] not in self._labels:
                    self._labels.update({row['label']: row['id']})
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
                        self._constants.update({column['constant_name']: column['length']})

        for label, label_id in sorted(self._labels.items()):
            self._constants.update({label: label_id})

# ----------------------------------------------------------------------------------------------------------------------
