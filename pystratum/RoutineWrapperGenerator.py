"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
import configparser
import json
import os

from pystratum.Util import Util


class RoutineWrapperGenerator:
    """
    Class for generating a class with wrapper methods for calling stored routines in a MySQL database.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._code = ''
        """
        The generated Python code buffer.

        :type: str
        """

        self._lob_as_string_flag = False
        """
        If true BLOBs and CLOBs must be treated as strings.

        :type: bool
        """

        self._metadata_filename = None
        """
        The filename of the file with the metadata of all stored procedures.

        :type: str
        """

        self._parent_class_name = None
        """
        The class name of the parent class of the routine wrapper.

        :type: str
        """

        self._parent_class_namespace = None
        """
        The namespace of the parent class of the routine wrapper.

        :type: str
        """

        self._wrapper_class_name = None
        """
        The class name of the routine wrapper.

        :type: str
        """

        self._wrapper_filename = None
        """
        The filename where the generated wrapper class must be stored.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def run(self, config_filename):
        """
        The "main" of the wrapper generator. Returns 0 on success, 1 if one or more errors occurred.

        :param str config_filename: The name of the configuration file.

        :rtype: int
        """
        self._read_configuration_file(config_filename)

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
    def _read_configuration_file(self, config_filename):
        """
        Reads parameters from the configuration file.

        :param str config_filename: The name of the configuration file.
        """
        config = configparser.ConfigParser()
        config.read(config_filename)

        self._parent_class_name = config.get('wrapper', 'parent_class')
        self._parent_class_namespace = config.get('wrapper', 'parent_class_namespace')
        self._wrapper_class_name = config.get('wrapper', 'wrapper_class')
        self._wrapper_filename = config.get('wrapper', 'wrapper_file')
        self._metadata_filename = config.get('wrapper', 'metadata')
        self._lob_as_string_flag = config.get('wrapper', 'lob_as_string')

    # ------------------------------------------------------------------------------------------------------------------
    def _read_routine_metadata(self):
        """
        Returns the metadata of stored routines.

        :rtype: dict
        """
        metadata = {}
        if os.path.isfile(self._metadata_filename):
            with open(self._metadata_filename, 'r') as file:
                metadata = json.load(file)

        return metadata

    # ------------------------------------------------------------------------------------------------------------------
    def _write_class_header(self):
        """
        Generate a class header for stored routine wrapper.
        """
        self._write_line("from {0!s} import {1!s}".format(self._parent_class_namespace, self._parent_class_name))
        self._write_line()
        self._write_line()
        self._write_line('# ' + ('-' * 118))
        self._write_line("class {0!s}({1!s}):".format(self._wrapper_class_name, self._parent_class_name))

    # ------------------------------------------------------------------------------------------------------------------
    def _write_line(self, text=''):
        """
        Writes a line with Python code to the generate code buffer.

        :param str text: The line with Python code.
        """
        if text:
            self._code += str(text) + "\n"
        else:
            self._code += "\n"

    # ------------------------------------------------------------------------------------------------------------------
    def _write_class_trailer(self):
        """
        Generate a class trailer for stored routine wrapper.
        """
        self._write_line()
        self._write_line()
        self._write_line('# ' + ('-' * 118))

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _write_routine_function(self, routine):
        """
        Generates a complete wrapper method for a stored routine.

        :param dict routine: The metadata of the stored routine.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
