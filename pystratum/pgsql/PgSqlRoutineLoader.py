from pystratum.RoutineLoader import RoutineLoader
from pystratum.pgsql.PgSqlConnection import PgSqlConnection
from pystratum.pgsql.PgSqlRoutineLoaderHelper import PgSqlRoutineLoaderHelper
from pystratum.pgsql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class PgSqlRoutineLoader(PgSqlConnection, RoutineLoader):
    """
    Class for loading stored routines into a PostgreSQL instance from (pseudo) SQL files.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        RoutineLoader.__init__(self)
        PgSqlConnection.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_column_type(self):
        """
        Selects schema, table, column names and the column type from MySQL and saves them as replace pairs.
        """
        sql = """
select table_name                                    "table_name"
,      column_name                                   "column_name"
,      udt_name                                      "column_type"
,      null                                          "table_schema"
from   information_schema.columns
where  table_catalog = current_database()
and    table_schema  = current_schema()

union all

select table_name                                    "table_name"
,      column_name                                   "column_name"
,      udt_name                                      "column_type"
,      table_schema                                  "table_schema"
from   information_schema.columns
where  table_catalog = current_database()
order by table_schema
,        table_name
,        column_name
"""

        rows = StaticDataLayer.execute_rows(sql)

        for row in rows:
            key = '@'
            if row['table_schema']:
                key += row['table_schema'] + '.'
            key += row['table_name'] + '.' + row['column_name'] + '%type@'
            key = key.lower()
            value = row['column_type']

            self._replace_pairs[key] = value

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_loader_helper(self, routine_name, pystratum_old_metadata, rdbms_old_metadata):
        """
        Creates a Routine Loader Helper object.

        :param str routine_name: The name of the routine.
        :param dict pystratum_old_metadata: The old metadata of the stored routine from PyStratum.
        :param dict rdbms_old_metadata:  The old metadata of the stored routine from PostgreSQL.

        :rtype: pystratum.pgsql.PgSqlRoutineLoaderHelper.PgSqlRoutineLoaderHelper
        """
        return PgSqlRoutineLoaderHelper(self._source_file_names[routine_name],
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
select t1.routine_name                                                                        routine_name
,      t1.routine_type                                                                        routine_type
,      array_to_string(array_agg(case when (parameter_name is not null) then
                                   concat(t2.parameter_mode, ' ',
                                          t2.parameter_name, ' ',
                                          t2.udt_name)
                                 end order by t2.ordinal_position asc), ',')                  routine_args
from            information_schema.routines   t1
left outer join information_schema.parameters t2  on  t2.specific_catalog = t1.specific_catalog and
                                                      t2.specific_schema  = t1.specific_schema and
                                                      t2.specific_name    = t1.specific_name and
                                                      t2.parameter_name   is not null
where routine_catalog = current_database()
and   routine_schema  = current_schema()
group by t1.routine_name
,        t1.routine_type
order by routine_name
"""

        rows = StaticDataLayer.execute_rows(query)
        self._rdbms_old_metadata = {}
        for row in rows:
            self._rdbms_old_metadata[row['routine_name']] = row

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_obsolete_routines(self):
        """
        Drops obsolete stored routines (i.e. stored routines that exists in the current schema but for
        which we don't have a source file).
        """
        for routine_name, values in self._rdbms_old_metadata.items():
            if routine_name not in self._source_file_names:
                print("Dropping {0!s} {1!s}".format(values['routine_type'], routine_name))
                sql = "drop {0!s} if exists {1!s}({2!s})".format(values['routine_type'],
                                                    routine_name,
                                                    values['routine_args'])
                StaticDataLayer.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def read_configuration_file(self, config_filename):
        """
        Reads parameters from the configuration file.

        :param string config_filename:
        """
        RoutineLoader.read_configuration_file(self, config_filename)
        PgSqlConnection.read_configuration_file(self, config_filename)

# ----------------------------------------------------------------------------------------------------------------------
