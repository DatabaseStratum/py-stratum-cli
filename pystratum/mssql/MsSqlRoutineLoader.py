from pystratum.RoutineLoader import RoutineLoader
from pystratum.mssql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlRoutineLoader(RoutineLoader):
    """
    Class for loading stored routines into a MySQL instance from pseudo SQL files.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def connect(self):
        """
        Connects to the database.
        """
        StaticDataLayer.connect(self._host_name,
                                self._user_name,
                                self._password,
                                self._database)

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self):
        """
        Disconnects from the database.
        """
        StaticDataLayer.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def _get_column_type(self):
        """
        Selects schema, table, column names and the column type from MySQL and saves them as replace pairs.
        """
        sql = """select scm.name  schema_name
,      tab.name  table_name
,      col.name  column_name
,      typ.name  type_name
,      col.max_length
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

        rows = StaticDataLayer.execute_rows(sql)

        for row in rows:
            key = '@'
            if row['schema_name']:
                key += row['schema_name'] + '.'
            key += row['table_name'] + '.' + row['column_name'] + '%type@'
            key = key.lower()
            value = row['type_name']

            self._replace_pairs[key] = value

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
and   prc.is_ms_shipped=0
;
"""

        rows = StaticDataLayer.execute_rows(query)

        self._old_stored_routines_info = {}
        for row in rows:
            self._old_stored_routines_info[row['procedure_name']] = row

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_obsolete_routines(self):
        """
        Drops obsolete stored routines (i.e. stored routines that exits in the current schema but for
        which we don't have a source file).
        """
        for routine_name, values in self._old_stored_routines_info.items():
            if routine_name not in self._source_file_names:
                # todo improve drop fun and proc
                print("Dropping %s.%s" % (values['schema_name'], routine_name))
                sql = "drop procedure %s.%s" % (values['schema_name'], routine_name)
                StaticDataLayer.execute_none(sql)

# ----------------------------------------------------------------------------------------------------------------------
