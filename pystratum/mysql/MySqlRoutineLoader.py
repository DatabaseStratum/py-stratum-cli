"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum.RoutineLoader import RoutineLoader
from pystratum.mysql.MySqlConnection import MySqlConnection
from pystratum.mysql.MySqlRoutineLoaderHelper import MySqlRoutineLoaderHelper
from pystratum.mysql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class MySqlRoutineLoader(MySqlConnection, RoutineLoader):
    """
    Class for loading stored routines into a MySQL instance from (pseudo) SQL files.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        RoutineLoader.__init__(self)
        MySqlConnection.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_column_type(self):
        """
        Selects schema, table, column names and the column type from MySQL and saves them as replace pairs.
        """
        sql = """
select TABLE_NAME                                    table_name
,      COLUMN_NAME                                   column_name
,      COLUMN_TYPE                                   column_type
,      CHARACTER_SET_NAME                            character_set_name
,      null                                          table_schema
from   information_schema.COLUMNS
where  TABLE_SCHEMA = database()
union all
select TABLE_NAME                                    table_name
,      COLUMN_NAME                                   column_name
,      COLUMN_TYPE                                   column_type
,      CHARACTER_SET_NAME                            character_set_name
,      TABLE_SCHEMA                                  table_schema
from   information_schema.COLUMNS
order by table_schema
,        table_name
,        column_name"""

        rows = StaticDataLayer.execute_rows(sql)

        for row in rows:
            key = '@'
            if row['table_schema']:
                key += row['table_schema'] + '.'
            key += row['table_name'] + '.' + row['column_name'] + '%type@'
            key = key.lower()
            value = row['column_type']

            if row['character_set_name']:
                value += ' character set ' + row['character_set_name']

            self._replace_pairs[key] = value

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_loader_helper(self, routine_name, pystratum_old_metadata, rdbms_old_metadata):
        """
        Creates a Routine Loader Helper object.

        :param str routine_name: The name of the routine.
        :param dict pystratum_old_metadata: The old metadata of the stored routine from PyStratum.
        :param dict rdbms_old_metadata:  The old metadata of the stored routine from MySQL.

        :rtype: pystratum.mysql.MySqlRoutineLoaderHelper.MySqlRoutineLoaderHelper
        """
        return MySqlRoutineLoaderHelper(self._source_file_names[routine_name],
                                        self._source_file_encoding,
                                        pystratum_old_metadata,
                                        self._replace_pairs,
                                        rdbms_old_metadata,
                                        self._sql_mode,
                                        self._character_set_client,
                                        self._collation_connection)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_old_stored_routine_info(self):
        """
        Retrieves information about all stored routines in the current schema.
        """
        query = """
select ROUTINE_NAME           routine_name
,      ROUTINE_TYPE           routine_type
,      SQL_MODE               sql_mode
,      CHARACTER_SET_CLIENT   character_set_client
,      COLLATION_CONNECTION   collation_connection
from  information_schema.ROUTINES
where ROUTINE_SCHEMA = database()
order by routine_name"""

        rows = StaticDataLayer.execute_rows(query)
        self._rdbms_old_metadata = {}
        for row in rows:
            self._rdbms_old_metadata[row['routine_name']] = row

    # ------------------------------------------------------------------------------------------------------------------
    def _get_correct_sql_mode(self):
        """
        Gets the SQL mode in the order as preferred by MySQL.
        """
        sql = "set sql_mode = {0!s}".format(self._sql_mode)
        StaticDataLayer.execute_none(sql)

        query = "select @@sql_mode;"
        tmp = StaticDataLayer.execute_rows(query)
        self._sql_mode = tmp[0]['@@sql_mode']

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_obsolete_routines(self):
        """
        Drops obsolete stored routines (i.e. stored routines that exits in the current schema but for
        which we don't have a source file).
        """
        for routine_name, values in self._rdbms_old_metadata.items():
            if routine_name not in self._source_file_names:
                print("Dropping {0!s} {1!s}".format(values['routine_type'], routine_name))
                sql = "drop {0!s} if exists {1!s}".format(values['routine_type'], routine_name)
                StaticDataLayer.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        :param config_filename string
        """
        RoutineLoader._read_configuration_file(self, config_filename)
        MySqlConnection._read_configuration_file(self, config_filename)

# ----------------------------------------------------------------------------------------------------------------------
