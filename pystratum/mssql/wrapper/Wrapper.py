import abc


# ----------------------------------------------------------------------------------------------------------------------
class Wrapper:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, routine, lob_as_string_flag):
        """
        :param routine: The metadata of the stored routine.
        """
        self.c_page_width = 120
        # must be constant
        self._code = ''
        self._indent_level = 1
        self._routine = routine

        self._lob_as_string_flag = False

        if lob_as_string_flag == 'True':
            self._lob_as_string_flag = True

    # ------------------------------------------------------------------------------------------------------------------
    def _write(self, line):
        self._code += str(line)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_line(self, line=None):
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
    def _indent_level_down(self, levels=None):
        if levels:
            self._indent_level -= int(levels)
        else:
            self._indent_level -= 1

    # ------------------------------------------------------------------------------------------------------------------
    def _write_separator(self):
        tmp = self.c_page_width - ((4 * self._indent_level) + 2)
        self._write_line('# ' + ('-' * tmp))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_blob_parameter(parameters):
        has_blob = False

        templates = {'tinytext': True, 'text': True, 'mediumtext': True, 'longtext': True, 'tinyblob': True,
                     'blob': True, 'mediumblob': True, 'longblob': True, 'tinyint': False, 'smallint': False,
                     'mediumint': False, 'int': False, 'bigint': False, 'year': False, 'decimal': False,
                     'float': False, 'double': False, 'time': False, 'timestamp': False, 'binary': False,
                     'enum': False, 'bit': False, 'set': False, 'char': False, 'varchar': False,
                     'date': False, 'datetime': False, 'varbinary': False}

        if parameters:

            for parameter_info in parameters:
                if parameter_info['data_type'] in templates:
                    has_blob = templates[parameter_info['data_type']]
                else:
                    print("Unknown MySQL type '%s'." % parameter_info['data_type'])

        return has_blob

    # ------------------------------------------------------------------------------------------------------------------
    def write_routine_method(self, routine):
        """
        Generates a complete wrapper method.
        :return: Python code with a routine wrapper.
        """
        if self._lob_as_string_flag:
            return self._write_routine_method_without_lob(routine)
        else:
            if self.is_blob_parameter(routine['parameters']):
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
        # todo  if routine['designation'] == 'bulk':
        #           ret = 'bulk_handler'  else:
        ret = ''

        for parameter_info in routine['parameters']:
            if ret:
                ret += ', '

            ret += parameter_info['name']

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def _generate_command(self, routine):
        if routine['parameters']:
            parameters = ''
            placeholders = ''
            for parameter in routine['parameters']:
                if parameters:
                    parameters += ', '
                    placeholders += ', '
                parameters += parameter['name']
                placeholders += '%s'
            ret = "'exec %s.%s %s' %% %s" % (routine['schema_name'],
                                             routine['routine_name'],
                                             placeholders,
                                             parameters)
        else:
            ret = "'exec %s.%s'" % (routine['schema_name'], routine['routine_name'])

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_re_type(data_type):

        lob = '%s'

        templates = {'tinyint': '%d', 'smallint': '%d', 'mediumint': '%d', 'int': '%d', 'bigint': '%d', 'year': '%d',
                     'decimal': '%d', 'float': '%d', 'double': '%d', 'varbinary': '%s', 'binary': '%s', 'char': '%s',
                     'varchar': '%s', 'time': '%s', 'timestamp': '%s', 'date': '%s', 'datetime': '%s', 'enum': '%s',
                     'set': '%s', 'bit': '%s', 'tinytext': lob, 'text': lob, 'mediumtext': lob, 'longtext': lob,
                     'tinyblob': lob, 'blob': lob, 'mediumblob': lob, 'longblob': lob}

        ret = '%s'
        if data_type in templates:
            ret = templates[data_type]
        else:
            print('Unknown data type %s.' % data_type)

        return ret


# ----------------------------------------------------------------------------------------------------------------------
