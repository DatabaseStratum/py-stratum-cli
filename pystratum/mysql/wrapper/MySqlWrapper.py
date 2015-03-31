import abc
from pystratum.wrapper.Wrapper import Wrapper


# ----------------------------------------------------------------------------------------------------------------------
class MySqlWrapper(Wrapper):
    """
    Parent class for classes that generate Python code, i.e. wrappers, for calling a stored routine.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def is_lob_parameter(self, parameters) -> bool:
        """
        Returns True of one of the parameters is a BLOB or CLOB. Otherwise, returns False.

        :param parameters: The parameters of a stored routine.
        :return:
        """
        has_lob = False

        lookup = {'bigint': False,
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
                if parameter_info['data_type'] in lookup:
                    has_lob = lookup[parameter_info['data_type']]
                else:
                    raise Exception("Unexpected date type '%s'." % parameter_info['data_type'])

        return has_lob

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _write_result_handler(self, routine):
        """
        Generates code for calling the stored routine in the wrapper method.
        """
        pass

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
        lookup = {'bigint': '%d',
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

        if data_type in lookup:
            return lookup[data_type]

        raise Exception('Unexpected data type %s.' % data_type)


# ----------------------------------------------------------------------------------------------------------------------
