"""
PyStratum
"""
import abc
import configparser
import json
import os
from typing import Optional, Dict, Any

from pystratum.style.PyStratumStyle import PyStratumStyle

from pystratum.Util import Util


class RoutineWrapperGenerator:
    """
    Class for generating a class with wrapper methods for calling stored routines in a MySQL database.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: PyStratumStyle):
        """
        Object constructor.

        :param PyStratumStyle io: The output decorator.
        """
        self._code: str = ''
        """
        The generated Python code buffer.
        """

        self._lob_as_string_flag: bool = False
        """
        If true BLOBs and CLOBs must be treated as strings.
        """

        self._metadata_filename: Optional[str] = None
        """
        The filename of the file with the metadata of all stored procedures.
        """

        self._parent_class_name: Optional[str] = None
        """
        The class name of the parent class of the routine wrapper.
        """

        self._parent_class_namespace: Optional[str] = None
        """
        The namespace of the parent class of the routine wrapper.
        """

        self._wrapper_class_name: Optional[str] = None
        """
        The class name of the routine wrapper.
        """

        self._wrapper_filename: Optional[str] = None
        """
        The filename where the generated wrapper class must be stored.
        """

        self._io: PyStratumStyle = io
        """
        The output decorator.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def main(self, config_filename: str) -> int:
        """
        The "main" of the wrapper generator. Returns 0 on success, 1 if one or more errors occurred.

        :param str config_filename: The name of the configuration file.

        :rtype: int
        """
        self._read_configuration_file(config_filename)

        if self._wrapper_class_name:
            self._io.title('Wrapper')

            self.__generate_wrapper_class()
        else:
            self._io.log_verbose('Wrapper not enabled')

        return 0

    # ------------------------------------------------------------------------------------------------------------------
    def __generate_wrapper_class(self) -> None:
        """
        Generates the wrapper class.
        """
        routines = self._read_routine_metadata()

        self._write_class_header()

        if routines:
            for routine_name in sorted(routines):
                if routines[routine_name]['designation'] != 'hidden':
                    self._write_routine_function(routines[routine_name])
        else:
            self._io.error('No files with stored routines found')

        self._write_class_trailer()

        Util.write_two_phases(self._wrapper_filename, self._code, self._io)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str) -> None:
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
    def _read_routine_metadata(self) -> Dict:
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
    def _write_class_header(self) -> None:
        """
        Generate a class header for stored routine wrapper.
        """
        self._write_line('from typing import Any, Dict, List, Optional')
        self._write_line()
        self._write_line('from {0!s} import {1!s}'.format(self._parent_class_namespace, self._parent_class_name))
        self._write_line()
        self._write_line()
        self._write_line('# ' + ('-' * 118))
        self._write_line('class {0!s}({1!s}):'.format(self._wrapper_class_name, self._parent_class_name))
        self._write_line('    """')
        self._write_line('    The stored routines wrappers.')
        self._write_line('    """')

    # ------------------------------------------------------------------------------------------------------------------
    def _write_line(self, text: str = '') -> None:
        """
        Writes a line with Python code to the generate code buffer.

        :param str text: The line with Python code.
        """
        if text:
            self._code += str(text) + "\n"
        else:
            self._code += "\n"

    # ------------------------------------------------------------------------------------------------------------------
    def _write_class_trailer(self) -> None:
        """
        Generate a class trailer for stored routine wrapper.
        """
        self._write_line()
        self._write_line()
        self._write_line('# ' + ('-' * 118))

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _write_routine_function(self, routine: Dict[str, Any]) -> None:
        """
        Generates a complete wrapper method for a stored routine.

        :param dict routine: The metadata of the stored routine.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
