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
        """
        Object constructor.
        """
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
            key = '@{0!s}.{1!s}.{2!s}%type@'.format(row['schema_name'], row['table_name'], row['column_name'])
            key = key.lower()

            value = self._derive_data_type(row)

            self._replace_pairs[key] = value

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_loader_helper(self, routine_name, pystratum_old_metadata, rdbms_old_metadata):
        """
        Creates a Routine Loader Helper object.

        :param str routine_name: The name of the routine.
        :param dict pystratum_old_metadata: The old metadata of the stored routine from PyStratum.
        :param dict rdbms_old_metadata:  The old metadata of the stored routine from MS SQL Server.

        :rtype: pystratum.mssql.MsSqlRoutineLoaderHelper.MsSqlRoutineLoaderHelper
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
select scm.name    schema_name
,      prc.name    routine_name
,      prc.type  routine_type
from       sys.all_objects  prc
inner join sys.schemas     scm  on   scm.schema_id = prc.schema_id
where prc.type in ('P','FN','TF')
and   scm.name <> 'sys'
and   prc.is_ms_shipped=0"""

        rows = StaticDataLayer.execute_rows(query)

        self._rdbms_old_metadata = {}
        for row in rows:
            self._rdbms_old_metadata[row['schema_name'] + '.' + row['routine_name']] = row

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_obsolete_routines(self):
        """
        Drops obsolete stored routines (i.e. stored routines that exits in the current schema but for
        which we don't have a source file).
        """
        for routine_name, values in self._rdbms_old_metadata.items():
            if routine_name not in self._source_file_names:
                if values['routine_type'].strip() == 'P':
                    print("Dropping procedure {0!s}.{1!s}".format(values['schema_name'], values['routine_name']))
                    sql = "drop procedure [{0!s}].[{1!s}]".format(values['schema_name'], values['routine_name'])
                elif values['routine_type'].strip() in ('FN', 'TF'):
                    print("Dropping function {0!s}.{1!s}".format(values['schema_name'], values['routine_name']))
                    sql = "drop function [{0!s}].[{1!s}]".format(values['schema_name'], values['routine_name'])
                else:
                    raise Exception("Unknown routine type '{0!s}'.".format(values['type']))

                StaticDataLayer.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _derive_data_type(column):
        """
        Returns the proper SQL declaration of a data type of a column.

        :param dict column: The column of which the field is based.

        :rtype: str
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
            return 'decimal({0:d},{1:d})'.format(column['precision'], column['scale'])

        if data_type == 'numeric':
            return 'decimal({0:d},{1:d})'.format(column['precision'], column['scale'])

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
            return 'char({0:d})'.format(column['max_length'])

        if data_type == 'varchar':
            if column['max_length'] == -1:
                return 'varchar(max)'

            return 'varchar({0:d})'.format(column['max_length'])

        if data_type == 'text':
            return data_type

        if data_type == 'nchar':
            return 'nchar({0:d})'.format((column['max_length'] / 2))

        if data_type == 'nvarchar':
            if column['max_length'] == -1:
                return 'nvarchar(max)'

            return 'nvarchar({0:d})'.format((column['max_length'] / 2))

        if data_type == 'ntext':
            return data_type

        if data_type == 'binary':
            return data_type

        if data_type == 'varbinary':
            return 'varbinary({0:d})'.format(column['max_length'])

        if data_type == 'image':
            return data_type

        if data_type == 'xml':
            return data_type

        if data_type == 'geography':
            return data_type

        if data_type == 'geometry':
            return data_type

        raise Exception("Unexpected data type '{0!s}'.".format(data_type))

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename):
        """
        Reads parameters from the configuration file.

        :param str config_filename: The name of the configuration file.
        """
        RoutineLoader._read_configuration_file(self, config_filename)
        MsSqlConnection._read_configuration_file(self, config_filename)

# ----------------------------------------------------------------------------------------------------------------------
