from pystratum.RoutineLoader import RoutineLoader
from pystratum.mysql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class MySqlRoutineLoader(RoutineLoader):
    """
    Class for loading stored routines into a MySQL instance from (pseudo) SQL files.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def connect(self):
        """
        Connects to the MySQL instance.
        """
        StaticDataLayer.config['user'] = self._user_name
        StaticDataLayer.config['password'] = self._password
        StaticDataLayer.config['database'] = self._database
        StaticDataLayer.config['charset'] = self._character_set
        StaticDataLayer.config['collation'] = self._collate
        StaticDataLayer.config['sql_mode'] = self._sql_mode
        StaticDataLayer.connect()

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self):
        """
        Disconnects from the MySQL instance.
        """
        StaticDataLayer.disconnect()

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
,      NULL                                          table_schema
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

            self._replace_pairs.update({key: value})

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
        self._old_stored_routines_info = {}
        for row in rows:
            self._old_stored_routines_info.update({row['routine_name']: row})

    # ------------------------------------------------------------------------------------------------------------------
    def _get_correct_sql_mode(self):
        """
        Gets the SQL mode in the order as preferred by MySQL.
        """
        sql = "set sql_mode = %s" % self._sql_mode
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
        for routine_name, values in self._old_stored_routines_info.items():
            if routine_name not in self._source_file_names:
                print("Dropping %s %s" % (values['routine_type'], routine_name))
                sql = "drop %s if exists %s" % (values['routine_type'], routine_name)
                StaticDataLayer.execute_none(sql)


# ----------------------------------------------------------------------------------------------------------------------
