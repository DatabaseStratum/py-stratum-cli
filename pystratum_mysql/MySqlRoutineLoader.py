"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum.RoutineLoader import RoutineLoader
from pystratum_mysql.MetadataDataLayer import MetadataDataLayer

from pystratum_mysql.MySqlConnection import MySqlConnection
from pystratum_mysql.MySqlRoutineLoaderHelper import MySqlRoutineLoaderHelper


class MySqlRoutineLoader(MySqlConnection, RoutineLoader):
    """
    Class for loading stored routines into a MySQL instance from (pseudo) SQL files.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io):
        """
        Object constructor.

        :param pystratum.style.PyStratumStyle.PyStratumStyle io: The output decorator.
        """
        RoutineLoader.__init__(self, io)
        MySqlConnection.__init__(self, io)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_column_type(self):
        """
        Selects schema, table, column names and the column type from MySQL and saves them as replace pairs.
        """
        rows = MetadataDataLayer.get_all_table_columns()
        for row in rows:
            key = '@' + row['table_name'] + '.' + row['column_name'] + '%type@'
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

        :rtype: pystratum_mysql.MySqlRoutineLoaderHelper.MySqlRoutineLoaderHelper
        """
        return MySqlRoutineLoaderHelper(self._source_file_names[routine_name],
                                        self._source_file_encoding,
                                        pystratum_old_metadata,
                                        self._replace_pairs,
                                        rdbms_old_metadata,
                                        self._sql_mode,
                                        self._character_set_client,
                                        self._collation_connection,
                                        self._io)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_old_stored_routine_info(self):
        """
        Retrieves information about all stored routines in the current schema.
        """
        rows = MetadataDataLayer.get_routines()
        self._rdbms_old_metadata = {}
        for row in rows:
            self._rdbms_old_metadata[row['routine_name']] = row

    # ------------------------------------------------------------------------------------------------------------------
    def _get_correct_sql_mode(self):
        """
        Gets the SQL mode in the order as preferred by MySQL.
        """
        self._sql_mode = MetadataDataLayer.get_correct_sql_mode(self._sql_mode)

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_obsolete_routines(self):
        """
        Drops obsolete stored routines (i.e. stored routines that exits in the current schema but for
        which we don't have a source file).
        """
        for routine_name, values in self._rdbms_old_metadata.items():
            if routine_name not in self._source_file_names:
                self._io.writeln("Dropping {0} <dbo>{1}</dbo>".format(values['routine_type'].lower(), routine_name))
                MetadataDataLayer.drop_stored_routine(values['routine_type'], routine_name)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        :param config_filename string
        """
        RoutineLoader._read_configuration_file(self, config_filename)
        MySqlConnection._read_configuration_file(self, config_filename)

# ----------------------------------------------------------------------------------------------------------------------
