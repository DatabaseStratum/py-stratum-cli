# ----------------------------------------------------------------------------------------------------------------------
class RoutineLoader:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        # The default character set under which the stored routine will be loaded and run.
        self._character_set = ''

        # The default collate under which the stored routine will be loaded and run.
        self._collate = ''

        # The database name.
        self._database = ''

        # A list with source names that are not loaded into MySQL.
        self.error_file_names = []

        # The hostname of the MySQL instance.
        self._host_name = ''

        # The meta data of all stored routines.
        self._metadata = {}

        # The filename of the file with the metadata of all stored routines.
        self._metadata_filename = ''

        # Old metadata about all stored routines.
        self._old_stored_routines_info = {}

        # Password required for logging in on to the MySQL instance.
        self._password = ''

        # A map from placeholders to their actual values.
        self._replace_pairs = {}

        # Path where source files can be found.
        self._source_directory = ''

        # The extension of the source files.
        self._source_file_extension = ''

        # All found source files.
        self._source_file_names = []

        # The SQL mode under which the stored routine will be loaded and run.
        self._sql_mode = ''

        # The name of the configuration file of the target project.
        self._target_config_filename = ''

        # User name.
        self._user_name = ''

    # ------------------------------------------------------------------------------------------------------------------
    def main(self, config_filename, file_names=None):
        """
        Loads stored routines into the current schema.
        :param config_filename: The name of the configuration file of the current project
        :param file_names: The sources that must be loaded. If empty all sources (if required) will loaded.
        :rtype : int
        """
        print('Hello nurse.')

        return 0 if not self.error_file_names else 1


# ----------------------------------------------------------------------------------------------------------------------
