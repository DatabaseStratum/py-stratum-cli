"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
import os


class Wrapper(metaclass=abc.ABCMeta):
    """
    Parent class for classes that generate Python code, i.e. wrappers, for calling a stored procedures and functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, routine, lob_as_string_flag):
        """
        Object constructor.

        :param dict routine: The metadata of the stored routine.
        :param str lob_as_string_flag: If 'True' LOBs must be treated as strings/bytes.
        """
        self._page_width = 120
        """
        The maximum number of columns in the source code.

        :type: int
        """

        self._code = ''
        """
        Buffer for the generated code.

        :type: str
        """

        self.__indent_level = 1
        """
        The current level of indentation in the generated code.

        :type: int
        """

        self._routine = routine
        """
        The metadata of the stored routine.

        :type: dict
        """

        self._lob_as_string_flag = lob_as_string_flag == 'True'
        """
        If True BLOBs and CLOBs must be treated as strings.

        :type: bool
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _write(self, text):
        """
        Appends a part of code to the generated code.

        :param str text: The part of code that must be appended.
        """
        self._code += str(text)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_line(self, line=None):
        """
        Appends a line of code to the generated code and adjust the indent level of the generated code.

        :param line: The line of code (with out LF) that must be appended.
        """
        if line is None:
            self._write("\n")
            if self.__indent_level > 1:
                self.__indent_level -= 1
        elif line == '':
            self._write("\n")
        else:
            line = (' ' * 4 * self.__indent_level) + line
            if line[-1:] == ':':
                self.__indent_level += 1
            self._write(line + "\n")

    # ------------------------------------------------------------------------------------------------------------------
    def _indent_level_down(self, levels=1):
        """
        Decrements the indent level of the generated code.

        :param levels: The number of levels indent level of the generated code must be decremented.
        """
        self.__indent_level -= int(levels)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_separator(self):
        """
        Inserts a horizontal (commented) line tot the generated code.
        """
        tmp = self._page_width - ((4 * self.__indent_level) + 2)
        self._write_line('# ' + ('-' * tmp))

    # ------------------------------------------------------------------------------------------------------------------
    def is_lob_parameter(self, parameters):
        """
        Returns True of one of the parameters is a BLOB or CLOB. Otherwise, returns False.

        :param parameters: The parameters of a stored routine.

        :rtype: bool
        """
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    def write_routine_method(self, routine):
        """
        Returns a complete wrapper method.

        :param dict[str,*] routine: The routine metadata.

        :rtype: str
        """
        if self._lob_as_string_flag:
            return self._write_routine_method_without_lob(routine)
        else:
            if self.is_lob_parameter(routine['parameters']):
                return self._write_routine_method_with_lob(routine)
            else:
                return self._write_routine_method_without_lob(routine)

    # ------------------------------------------------------------------------------------------------------------------
    def __write_docstring_description(self, routine):
        """
        Writes the description part of the docstring for the wrapper method of a stored routine.

        :param dict routine: The metadata of the stored routine.
        """
        if routine['pydoc']['description']:
            self._write_line(routine['pydoc']['description'])

    # ------------------------------------------------------------------------------------------------------------------
    def __write_docstring_parameters(self, routine):
        """
        Writes the parameters part of the docstring for the wrapper method of a stored routine.

        :param dict routine: The metadata of the stored routine.
        """
        if routine['pydoc']['parameters']:
            self._write_line('')

            for param in routine['pydoc']['parameters']:
                lines = param['description'].split(os.linesep)
                self._write_line(':param {0} {1}: {2}'.format(param['python_type'],
                                                              param['parameter_name'],
                                                              lines[0]))
                del lines[0]

                tmp = ':param {0} {1}:'.format(param['python_type'], param['parameter_name'])
                indent = ' ' * len(tmp)
                for line in lines:
                    self._write_line('{0} {1}'.format(indent, line))

                self._write_line('{0} {1}'.format(indent, param['data_type_descriptor']))

    # ------------------------------------------------------------------------------------------------------------------
    def __write_docstring_return_type(self):
        """
        Writes the return type part of the docstring for the wrapper method of a stored routine.
        """
        rtype = self._get_docstring_return_type()
        if rtype:
            self._write_line('')
            self._write_line(':rtype: {0}'.format(rtype))

    # ------------------------------------------------------------------------------------------------------------------
    def __write_docstring(self, routine):
        """
        Writes the docstring for the wrapper method of a stored routine.

        :param dict routine: The metadata of the stored routine.
        """
        self._write_line('"""')

        self.__write_docstring_description(routine)
        self.__write_docstring_parameters(routine)
        self.__write_docstring_return_type()

        self._write_line('"""')

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_docstring_return_type(self):
        """
        Returns the return type of the wrapper methods the be used in the docstring.

        :rtype: str
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _write_result_handler(self, routine):
        """
        Generates code for calling the stored routine in the wrapper method.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _write_routine_method_with_lob(self, routine):
        return self._write_routine_method_without_lob(routine)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_routine_method_without_lob(self, routine):

        self._write_line()
        self._write_separator()
        self._write_line('@staticmethod')
        self._write_line('def {0!s}({1!s}):'.format(str(routine['routine_name']), str(self._get_wrapper_args(routine))))
        self.__write_docstring(routine)
        self._write_result_handler(routine)

        return self._code

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_wrapper_args(routine):
        """
        Returns code for the parameters of the wrapper method for the stored routine.

        :param dict[str,*] routine: The routine metadata.

        :rtype: str
        """
        # todo  if routine['designation'] == 'bulk':
        # ret = 'bulk_handler'  else:
        ret = ''

        for parameter_info in routine['parameters']:
            if ret:
                ret += ', '

            ret += parameter_info['name']

        return ret

# ----------------------------------------------------------------------------------------------------------------------
