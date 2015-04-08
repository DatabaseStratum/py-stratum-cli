from pystratum.RoutineLoader import RoutineLoader
from pystratum.mssql.MsSqlConnection import MsSqlConnection
from pystratum.mssql.MsSqlRoutineLoaderHelper import MsSqlRoutineLoaderHelper
from pystratum.mssql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlRoutineLoader(MsSqlConnection, RoutineLoader):
    """
    Class for loading stored routines into a MySQL instance from pseudo SQL files.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        RoutineLoader.__init__(self)
        MsSqlConnection.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_column_type(self):
        """
        Selects schema, table, column names and the column types from the SQL Server instance and saves them as replace
        pairs.
        """
        sql = """

select scm.name                   schema_name
,      tab.name                   table_name
,      col.name                   column_name
,      isnull(stp.name,utp.name)  data_type
,      col.max_length
,      col.precision
,      col.scale
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

        rows = StaticDataLayer.execute_rows(sql)

        for row in rows:
            key = '@'
            if row['schema_name']:
                key += row['schema_name'] + '.'
            key += row['table_name'] + '.' + row['column_name'] + '%type@'
            key = key.lower()

            value = self._derive_data_type(row)

            self._replace_pairs[key] = value

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_loader_helper(self,
                                     routine_name: str,
                                     pystratum_old_metadata: dict,
                                     rdbms_old_metadata: dict) -> MsSqlRoutineLoaderHelper:
        """
        Creates a Routine Loader Helper object.
        :return: A MsSqlRoutineLoaderHelper object.
        """
        return MsSqlRoutineLoaderHelper(self._source_file_names[routine_name],
                                        self._source_file_encoding,
                                        pystratum_old_metadata,
                                        self._replace_pairs,
                                        rdbms_old_metadata)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_old_stored_routine_info(self):
        """
        Retrieves information about all stored routines in the current schema.
        """
        query = """
select scm.name  schema_name
,      prc.name  procedure_name
,      prc.[type]  [type]
from       sys.all_objects  prc
inner join sys.schemas     scm  on   scm.schema_id = prc.schema_id
where prc.type in ('P','FN')
and   scm.name <> 'sys'
and   prc.is_ms_shipped=0"""

        rows = StaticDataLayer.execute_rows(query)

        self._rdbms_old_metadata = {}
        for row in rows:
            self._rdbms_old_metadata[row['procedure_name']] = row

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_obsolete_routines(self):
        """
        Drops obsolete stored routines (i.e. stored routines that exits in the current schema but for
        which we don't have a source file).
        """
        for routine_name, values in self._rdbms_old_metadata.items():
            if routine_name not in self._source_file_names:
                if values['type'].strip() == 'P':
                    print("Dropping procedure %s.%s" % (values['schema_name'], routine_name))
                    sql = "drop procedure [%s].[%s]" % (values['schema_name'], routine_name)
                elif values['type'].strip() == 'FN':
                    print("Dropping function %s.%s" % (values['schema_name'], routine_name))
                    sql = "drop function [%s].[%s]" % (values['schema_name'], routine_name)
                else:
                    raise Exception("Unknown routine type '%s'." % values['type'])

                StaticDataLayer.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _derive_data_type(column: dict) -> int:
        """
        Returns the proper SQL declaration of a data type of a column.
        :param column dict The column of which the field is based.
        :returns SQL declaration of data type
        """
        data_type = column['data_type']

        if data_type == 'bigint':
            return data_type

        if data_type == 'int':
            return data_type

        if data_type == 'smallint':
            return data_type

        if data_type == 'tinyint':
            return data_type

        if data_type == 'bit':
            return data_type

        if data_type == 'money':
            return data_type

        if data_type == 'smallmoney':
            return data_type

        if data_type == 'decimal':
            return 'decimal(%d,%d)' % (column['precision'], column['scale'])

        if data_type == 'numeric':
            return 'decimal(%d,%d)' % (column['precision'], column['scale'])

        if data_type == 'float':
            return data_type

        if data_type == 'real':
            return data_type

        if data_type == 'date':
            return data_type

        if data_type == 'datetime':
            return data_type

        if data_type == 'datetime2':
            return data_type

        if data_type == 'datetimeoffset':
            return data_type

        if data_type == 'smalldatetime':
            return data_type

        if data_type == 'time':
            return data_type

        if data_type == 'char':
            return 'char(%d)' % column['max_length']

        if data_type == 'varchar':
            if column['max_length'] == -1:
                return 'varchar(max)'

            return 'varchar(%d)' % column['max_length']

        if data_type == 'text':
            return data_type

        if data_type == 'nchar':
            return 'nchar(%d)' % (column['max_length'] / 2)

        if data_type == 'nvarchar':
            if column['max_length'] == -1:
                return 'nvarchar(max)'

            return 'nvarchar(%d)' % (column['max_length'] / 2)

        if data_type == 'ntext':
            return data_type

        if data_type == 'binary':
            return data_type

        if data_type == 'varbinary':
            return 'varbinary(%d)' % column['max_length']

        if data_type == 'image':
            return data_type

        if data_type == 'xml':
            return data_type

        if data_type == 'geography':
            return data_type

        if data_type == 'geometry':
            return data_type

        raise Exception("Unexpected data type '%s'." % data_type)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        :param config_filename string
        """
        RoutineLoader._read_configuration_file(self, config_filename)
        MsSqlConnection._read_configuration_file(self, config_filename)

# ----------------------------------------------------------------------------------------------------------------------

