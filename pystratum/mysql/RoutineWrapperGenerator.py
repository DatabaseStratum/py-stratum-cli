import configparser
import json
import os

from pystratum.Util import Util
from pystratum.mysql.wrapper import create_routine_wrapper


# ----------------------------------------------------------------------------------------------------------------------
class RoutineWrapperGenerator():
    """
    Class for generating a class with wrapper methods for calling stored routines in a MySQL database.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._code = ''
        """
        The generated PHP code.

        :type: string
        """
        self._configuration_filename = None
        """
        The filename of the configuration file.

        :type: var string
        """

        self._host_name = None
        """
        Host name or address.

        @var string
        """

        self._lob_as_string_flag = False
        """
        If true BLOBs and CLOBs must be treated as strings.
       
        :type: bool
        """

        self._metadata_filename = None
        """
        The filename of the file with the metadata of all stored procedures.
       
        :type: string
        """

        self._parent_class_name = None
        """
        The class name (including namespace) of the parent class of the routine wrapper.
       
        :type: string
        """

        self._password = None
        """
        The password.
       
        :type: string
        """

        self._user_name = None
        """
        The user name.
       
        :type: string
        """

        self._wrapper_class_name = None
        """
        The class name (including namespace) of the routine wrapper.
       
        :type: string
        """

        self._wrapper_filename = None
        """
        The filename where the generated wrapper class must be stored
       
        :type: string
        """

        self._password = None
        """
        Password required for logging in on to the MySQL instance.

        :type: string
        """

        self._database = None
        """
        The database name.

        :type: string
        """

    # ------------------------------------------------------------------------------------------------------------------
    def run(self, configuration_filename) -> bool:
        """
        The "main" of the wrapper generator.

        :param configuration_filename The name of the configuration file.
        :return Returns 0 on success, 1 if one or more errors occurred.
        """
        self._configuration_filename = configuration_filename
        self._read_configuration_file()

        routines = self._read_routine_metadata()

        self._write_class_header()

        if routines:
            for routine_name in sorted(routines):
                if routines[routine_name]['designation'] != 'hidden':
                    self._write_routine_function(routines[routine_name])
        else:
            print("No files with stored routines found.")

        self._write_class_trailer()

        Util.write_two_phases(self._wrapper_filename, self._code)

        return 0

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self):
        """
        Reads parameters from the configuration file.
        """
        config = configparser.ConfigParser()
        config.read(self._configuration_filename)

        self._host_name = config.get('database', 'host_name')
        self._user_name = config.get('database', 'user_name')
        self._password = config.get('database', 'password')
        self._database = config.get('database', 'database_name')

        self._parent_class_name = config.get('wrapper', 'parent_class')
        self._parent_class_namespace = config.get('wrapper', 'parent_class_namespace')
        self._wrapper_class_name = config.get('wrapper', 'wrapper_class')
        self._wrapper_filename = config.get('wrapper', 'wrapper_file')
        self._metadata_filename = config.get('wrapper', 'metadata')
        self._lob_as_string_flag = config.get('wrapper', 'lob_as_string')

        self._sql_mode = config.get('loader', 'sql_mode')
        self._character_set = config.get('loader', 'character_set')
        self._collate = config.get('loader', 'collate')

    # ------------------------------------------------------------------------------------------------------------------
    def _read_routine_metadata(self) -> dict:
        """
        Returns the metadata of stored routines.
        @return
        """
        metadata = {}
        if os.path.isfile(self._metadata_filename):
            with open(self._metadata_filename, 'r') as f:
                metadata = json.load(f)

        return metadata

    # ------------------------------------------------------------------------------------------------------------------
    def _write_class_header(self):
        """
        Generate a class header for stored routine wrapper.
        """
        self._write_line("from %s import %s" % (self._parent_class_namespace, self._parent_class_name))
        self._write_line()
        self._write_line()
        self._write_line('# ' + ('-'*118))
        self._write_line("class %s(%s):" % (self._wrapper_class_name, self._parent_class_name))

    # ------------------------------------------------------------------------------------------------------------------
    def _write_line(self, text=None):
        if text:
            self._code += str(text + "\n")
        else:
            self._code += "\n"

    # ------------------------------------------------------------------------------------------------------------------
    def _write_class_trailer(self):
        """
        Generate a class trailer for stored routine wrapper.
        """
        self._write_line()
        self._write_line()
        self._write_line('# ' + ('-'*118))

    # ------------------------------------------------------------------------------------------------------------------
    def _write_routine_function(self, routine):
        """
        Generates a complete wrapper method for a stored routine.
        :param  The metadata of the stored routine.
        """
        wrapper = create_routine_wrapper(routine, self._lob_as_string_flag)
        # xxx tmp
        if wrapper:
            self._code += wrapper.write_routine_method(routine)


# ----------------------------------------------------------------------------------------------------------------------
