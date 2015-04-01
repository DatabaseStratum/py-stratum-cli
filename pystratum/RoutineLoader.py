import abc
import os
from pprint import pprint
import re
import sys
import json
import configparser


# ----------------------------------------------------------------------------------------------------------------------
from pystratum.RoutineLoaderHelper import RoutineLoaderHelper


class RoutineLoader:
    """
    Class for loading stored routines into a RDBMS instance from (pseudo) SQL files.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._character_set = None
        """
        The default character set under which the stored routine will be loaded and run.

        :type: string
        """

        self._collate = None
        """
        The default collate under which the stored routine will be loaded and run.

        :type: string
        """

        self._database = None
        """
        The database name.

        :type: string
        """

        self.error_file_names = set()
        """
        A set with source names that are not loaded into RDBMS instance.

        :type: set
        """

        self._host_name = None
        """
        The hostname required connection to the MySQL instance.

        :type: string
        """

        self._metadata = {}
        """
        The meta data of all stored routines.

        :type: dict
        """

        self._metadata_filename = None
        """
        The filename of the file with the metadata of all stored routines.

        :type: string
        """

        self._old_stored_routines_info = {}
        """
        Old metadata about all stored routines.

        :type: dict
        """

        self._password = None
        """
        Password required for connection to the MySQL instance.

        :type: string
        """

        self._replace_pairs = {}
        """
        A map from placeholders to their actual values.

        :type: dict
        """

        self._source_directory = None
        """
        Path where source files can be found.

        :type: string
        """

        self._source_file_extension = None
        """
        The extension of the source files.

        :type: string
        """

        self._source_file_names = {}
        """
        All found source files.

        :type: dict
        """

        self._sql_mode = None
        """
        The SQL mode under which the stored routine will be loaded and run.

        :type: string
        """

        self._target_config_filename = None
        """
        The name of the configuration file of the target project.

        :type: string
        """

        self._user_name = None
        """
        User name required for connection to the MySQL instance..

        :type: string
        """

        self._constants_filename = None
        """

        :type: string
        """

    # ------------------------------------------------------------------------------------------------------------------
    def main(self, config_filename: str, file_names=None) -> int:
        """
        Loads stored routines into the current schema.
        :param config_filename: The name of the configuration file of the current project
        :param file_names: The sources that must be loaded. If empty all sources (if required) will loaded.
        :rtype : int The status of exit.
        """
        if file_names:
            self._load_list(config_filename, file_names)
        else:
            self._load_all(config_filename)

        if self.error_file_names:
            self._log_overview_errors()
            return 1
        else:
            return 0

    # ------------------------------------------------------------------------------------------------------------------
    def _log_overview_errors(self):
        """
        Show info about sources files of stored routines that were not loaded successfully.
        """
        for filename in sorted(self.error_file_names):
            print("Error loading file '%s'." % filename)

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def connect(self):
        """
        Connects to the RDBMS instance.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def disconnect(self):
        """
        Disconnects from the RDBMS instance.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _load_list(self, config_filename: str, file_names: list):
        """
        Loads all stored routines in a list into the RDBMS instance.
        :param config_filename The filename of the configuration file.
        :param file_names The list of files to be loaded.
        """
        self._read_configuration_file(config_filename)
        self.connect()
        self.find_source_files_from_list(file_names)
        self._get_column_type()
        self._read_stored_routine_metadata()
        self._get_constants()
        self._get_old_stored_routine_info()
        self._get_correct_sql_mode()
        self._load_stored_routines()
        self._write_stored_routine_metadata()
        self.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def _load_all(self, config_filename: str):
        """
        Loads all stored routines into the RDBMS instance.
        :param config_filename string The filename of the configuration file.
        """
        self._read_configuration_file(config_filename)
        self.connect()
        self._find_source_files()
        self._get_column_type()
        self._read_stored_routine_metadata()
        self._get_constants()
        self._get_old_stored_routine_info()
        self._get_correct_sql_mode()
        self._load_stored_routines()
        self._drop_obsolete_routines()
        self._remove_obsolete_metadata()
        self._write_stored_routine_metadata()
        self.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        :param config_filename string
        """
        config = configparser.ConfigParser()
        config.read(config_filename)

        rdbms = config.get('database', 'rdbms')
        self._host_name = config.get('database', 'host_name')
        self._user_name = config.get('database', 'user_name')
        self._password = config.get('database', 'password')
        self._database = config.get('database', 'database_name')

        self._metadata_filename = config.get('wrapper', 'metadata')

        self._source_directory = config.get('loader', 'source_directory')
        self._source_file_extension = config.get('loader', 'extension')
        self._source_file_encoding = config.get('loader', 'encoding')
        self._target_config_filename = config.get('loader', 'config')

        if rdbms == 'mysql':
            self._sql_mode = config.get('loader', 'sql_mode')
            self._character_set = config.get('loader', 'character_set')
            self._collate = config.get('loader', 'collate')

        self._constants_filename = config.get('constants', 'config')

    # ------------------------------------------------------------------------------------------------------------------
    def _find_source_files(self):
        """
        Searches recursively for all source files in a directory.
        """
        for dir_path, dir_names, files in os.walk(self._source_directory):
            for name in files:
                if name.lower().endswith(self._source_file_extension):
                    basename = os.path.splitext(os.path.basename(name))[0]
                    relative_path = os.path.relpath(os.path.join(dir_path, name))

                    if basename in self._source_file_names:
                        print("Error: Files '%s' and '%s' have the same basename." %
                              (self._source_file_names[basename], relative_path), file=sys.stderr)
                        self.error_file_names.add(relative_path)
                    else:
                        self._source_file_names[basename] = relative_path

    # ------------------------------------------------------------------------------------------------------------------
    def _read_stored_routine_metadata(self):
        """
        Reads the metadata of stored routines from the metadata file.
        """
        if os.path.isfile(self._metadata_filename):
            with open(self._metadata_filename, 'r') as f:
                self._metadata = json.load(f)

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_column_type(self):
        """
        Selects schema, table, column names and the column type from the RDBMS instance and saves them as replace pairs.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def create_routine_loader_helper(self,
                                     routine_name: str,
                                     old_metadata: dict,
                                     old_routine_info: dict) -> RoutineLoaderHelper:
        """
        Creates a Routine Loader Helper object.
        :return:
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _load_stored_routines(self):
        """
        Loads all stored routines into the RDBMS instance instance.
        """
        for routine_name in sorted(self._source_file_names):
            if routine_name in self._metadata:
                old_metadata = self._metadata[routine_name]
            else:
                old_metadata = None

            if routine_name in self._old_stored_routines_info:
                old_routine_info = self._old_stored_routines_info[routine_name]
            else:
                old_routine_info = None

            routine_loader_helper = self.create_routine_loader_helper(routine_name, old_metadata, old_routine_info)
            metadata = routine_loader_helper.load_stored_routine()

            if not metadata:
                self.error_file_names.add(self._source_file_names[routine_name])
                if routine_name in self._metadata:
                    del (self._metadata[routine_name])
            else:
                self._metadata[routine_name] = metadata

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_old_stored_routine_info(self):
        """
        Retrieves information about all stored routines in the current schema.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _get_correct_sql_mode(self):
        """
        Gets the SQL mode in the order as preferred by MySQL. This method is specific for MySQL.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _drop_obsolete_routines(self):
        """
        Drops obsolete stored routines (i.e. stored routines that exits in the current schema but for
        which we don't have a source file).
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _remove_obsolete_metadata(self):
        """
        Removes obsolete entries from the metadata of all stored routines.
        """
        clean = {}
        for key, source_filename in self._source_file_names.items():
            if key in self._metadata:
                clean[key] = self._metadata[key]

        self._metadata = clean

    # ------------------------------------------------------------------------------------------------------------------
    def _write_stored_routine_metadata(self):
        """
        Writes the metadata of all stored routines to the metadata file.
        """
        with open(self._metadata_filename, 'w') as f:
            json.dump(self._metadata, f, indent=4, sort_keys=True)

    # ------------------------------------------------------------------------------------------------------------------
    def find_source_files_from_list(self, file_names):
        """
        Finds all source files that actually exists from a list of file names.
        :param file_names list The list of file names.
        """
        for file_name in file_names:
            if os.path.exists(file_name):
                routine_name = os.path.splitext(os.path.basename(file_name))[0]
                if routine_name not in self._source_file_names:
                    self._source_file_names[routine_name] = file_name
                else:
                    print("Error: Files '%s' and '%s' have the same basename." %
                          (self._source_file_names[routine_name], file_name), file=sys.stderr)
                    self.error_file_names.add(file_name)
            else:
                print("File not exists: '%s'." % file_name)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_constants(self):
        """
        Temp solution for replace constants.
        """
        if os.path.exists(self._constants_filename):
            with open(self._constants_filename, 'r') as f:
                for line in f:
                    if line.strip() != "\n":
                        p = re.compile('(?:(\w+)\s*=\s*(\w+))')
                        matches = p.findall(line)

                        if matches:
                            matches = matches[0]
                            name = '@' + matches[0].lower() + '@'
                            value = matches[1]
                            if name in self._replace_pairs:
                                raise Exception("Duplicate placeholder '%s'" % name)
                            self._replace_pairs.update({name: value})


# ----------------------------------------------------------------------------------------------------------------------
