import abc


# ----------------------------------------------------------------------------------------------------------------------
class Wrapper:
    """
    Parent class for classes that generate Python code, i.e. wrappers, for calling a stored routine.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, routine, lob_as_string_flag: bool):
        """
        :param routine: The metadata of the stored routine.
        """
        self.c_page_width = 120
        # must be constant

        self._code = ''
        """
        Buffer for the generated code.

        :type: str
        """

        self._indent_level = 1
        """
        The current level of indentation in the generated code.

        :type: int
        """

        self._routine = routine

        self._lob_as_string_flag = lob_as_string_flag == 'True'
        """
        If True BLOBs and CLOBs must be treated as strings.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _write(self, text: str):
        """
        Appends a part of code to the generated code.

        :param text: The part of code that must be appended.
        """
        self._code += str(text)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_line(self, line=None):
        """
        Appends a line of code to the generated code and adjust the indent level of the generated code.

        :param line: The line of code (with out LF) that must be appended.
        """
        if not line:
            self._write("\n")
            if self._indent_level > 1:
                self._indent_level -= 1
        else:
            line = (' ' * 4 * self._indent_level) + line
            if line[-1:] == ':':
                self._indent_level += 1
            self._write(line + "\n")

    # ------------------------------------------------------------------------------------------------------------------
    def _indent_level_down(self, levels=1):
        """
        Decrements the indent level of the generated code.

        :param levels: The number of levels indent level of the generated code must be decremented.
        """
        self._indent_level -= int(levels)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_separator(self):
        """
        Inserts a horizontal (commented) line tot the generated code.
        """
        tmp = self.c_page_width - ((4 * self._indent_level) + 2)
        self._write_line('# ' + ('-' * tmp))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_lob_parameter(parameters) -> bool:
        """
        Returns True of one of the parameters is a BLOB or CLOB. Otherwise, returns False.

        :param parameters: The parameters of a stored routine.
        :return:
        """
        has_lob = False

        lob_map = {'bigint': False,
                   'binary': False,
                   'bit': False,
                   'char': False,
                   'date': False,
                   'datetime': False,
                   'decimal': False,
                   'double': False,
                   'enum': False,
                   'float': False,
                   'int': False,
                   'mediumint': False,
                   'set': False,
                   'smallint': False,
                   'time': False,
                   'timestamp': False,
                   'tinyint': False,
                   'varbinary': False,
                   'varchar': False,
                   'year': False,

                   'blob': True,
                   'longblob': True,
                   'longtext': True,
                   'mediumblob': True,
                   'mediumtext': True,
                   'text': True,
                   'tinyblob': True,
                   'tinytext': True}

        if parameters:
            for parameter_info in parameters:
                if parameter_info['data_type'] in lob_map:
                    has_lob = lob_map[parameter_info['data_type']]
                else:
                    raise Exception("Unexpected date type '%s'." % parameter_info['data_type'])

        return has_lob

    # ------------------------------------------------------------------------------------------------------------------
    def write_routine_method(self, routine):
        """
        Generates a complete wrapper method.

        :return: Python code with a routine wrapper.
        """
        if self._lob_as_string_flag:
            return self._write_routine_method_without_lob(routine)
        else:
            if self.is_lob_parameter(routine['parameters']):
                return self._write_routine_method_with_lob(routine)
            else:
                return self._write_routine_method_without_lob(routine)

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _write_result_handler(self, routine):
        """
        Generates code for calling the stored routine in the wrapper method.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _write_routine_method_with_lob(self, routine):
        return ''

    # ------------------------------------------------------------------------------------------------------------------
    def _write_routine_method_without_lob(self, routine):

        self._write_line()
        self._write_separator()
        self._write_line('@staticmethod')
        self._write_line('def %s(%s):' % (str(routine['routine_name']), str(self._get_wrapper_args(routine))))
        self._write_result_handler(routine)

        return self._code

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_wrapper_args(routine):
        """
        Returns code for the parameters of the wrapper method for the stored routine.

        :param routine:
        :return: The Python snippet.
        """
        # todo  if routine['designation'] == 'bulk':
        # ret = 'bulk_handler'  else:
        ret = ''

        for parameter_info in routine['parameters']:
            if ret:
                ret += ', '

            ret += parameter_info['name']

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _generate_command(self, routine):
        """
        Generates SQL statement for calling a stored routine.

        :param routine: Metadata of the stored routine.
        :return: The generated SQL statement.
        """
        parameters = ''
        placeholders = ''

        execute = 'call'
        if routine['designation'] == 'function':
            execute = 'select'

        i = 0
        l = 0
        for parameter in routine['parameters']:
            re_type = self._get_parameter_format_specifier(parameter['data_type'])
            if parameters:
                parameters += ', '
                placeholders += ', '
            parameters += parameter['name']
            placeholders += re_type
            i += 1
            if not re_type == '?':
                l += 1

        if l == 0:
            line = '"%s %s()"' % (execute, routine['routine_name'])
        elif l >= 1:
            line = '"%s %s(%s)", %s' % (execute, routine['routine_name'], placeholders, parameters)
        else:
            raise Exception('Internal error.')

        return line

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_parameter_format_specifier(data_type: str):
        """
        Returns the appropriate format specifier for a parameter type.

        :param data_type: The parameter type.
        :return: The format specifier.
        """
        templates = {'bigint': '%d',
                     'binary': '%s',
                     'bit': '%s',
                     'blob': '%s',
                     'char': '%s',
                     'date': '%s',
                     'datetime': '%s',
                     'decimal': '%d',
                     'double': '%d',
                     'enum': '%s',
                     'float': '%d',
                     'int': '%d',
                     'longblob': '%s',
                     'longtext': '%s',
                     'mediumblob': '%s',
                     'mediumint': '%d',
                     'mediumtext': '%s',
                     'set': '%s',
                     'smallint': '%d',
                     'text': '%s',
                     'time': '%s',
                     'timestamp': '%s',
                     'tinyblob': '%s',
                     'tinyint': '%d',
                     'tinytext': '%s',
                     'varbinary': '%s',
                     'varchar': '%s',
                     'year': '%d'}

        if data_type in templates:
            return templates[data_type]

        raise Exception('Unexpected data type %s.' % data_type)


# ----------------------------------------------------------------------------------------------------------------------
