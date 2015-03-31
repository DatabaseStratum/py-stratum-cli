import abc
from pystratum.wrapper.Wrapper import Wrapper


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlWrapper(Wrapper):
    """
    Parent class for classes that generate Python code, i.e. wrappers, for calling a stored routine.
    """
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_blob_parameter(parameters):
        has_blob = False

        templates = {'bigint': False,
                     'binary': False,
                     'bit': False,
                     'char': False,
                     'date': False,
                     'datetime': False,
                     'datetime2': False,
                     'datetimeoffset': False,
                     'decimal': False,
                     'float': False,
                     'image': False,
                     'int': False,
                     'money': False,
                     'nchar': False,
                     'ntext': False,
                     'numeric': False,
                     'nvarchar': False,
                     'real': False,
                     'smalldatetime': False,
                     'smallint': False,
                     'smallmoney': False,
                     'text': False,
                     'time': False,
                     'tinyint': False,
                     'varbinary': False,
                     'varchar': False,
                     'xml': False}

        if parameters:
            for parameter_info in parameters:
                if parameter_info['data_type'] in templates:
                    has_blob = templates[parameter_info['data_type']]
                else:
                    print("Unknown SQL type '%s'." % parameter_info['data_type'])

        return has_blob

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
        if routine['parameters']:
            if routine['designation'] == 'function':
                sql = "'select %s.%s(%s)', %s"
            else:
                sql = "'exec %s.%s %s', %s"

            parameters = ''
            placeholders = ''
            for parameter in routine['parameters']:
                if parameters:
                    parameters += ', '
                    placeholders += ', '
                parameters += parameter['name']
                placeholders += self._get_parameter_format_specifier(parameter['data_type'])

            ret = sql % (routine['schema_name'],
                         routine['routine_name'],
                         placeholders,
                         parameters)
        else:
            if routine['designation'] == 'function':
                sql = "'select %s.%s()'"
            else:
                sql = "'exec %s.%s'"

            ret = sql % (routine['schema_name'],
                         routine['routine_name'])

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_parameter_format_specifier(data_type: str):
        """
        Returns the appropriate format specifier for a parameter type.

        :param data_type: The parameter type.
        :return: The format specifier.
        """
        templates = {'bigint': '%s',
                     'binary': '%s',
                     'bit': '%s',
                     'char': '%s',
                     'date': '%s',
                     'datetime': '%s',
                     'datetime2': '%s',
                     'datetimeoffset': '%s',
                     'decimal': '%s',
                     'float': '%s',
                     'image': '%s',
                     'int': '%s',
                     'money': '%s',
                     'nchar': '%s',
                     'ntext': '%s',
                     'numeric': '%s',
                     'nvarchar': '%s',
                     'real': '%s',
                     'smalldatetime': '%s',
                     'smallint': '%s',
                     'smallmoney': '%s',
                     'text': '%s',
                     'time': '%s',
                     'tinyint': '%s',
                     'varbinary': '%s',
                     'varchar': '%s',
                     'xml': '%s'}

        if data_type in templates:
            return '%s'

        raise Exception('Unexpected data type %s.' % data_type)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_re_type(data_type):

        lob = '%s'

        templates = {'bigint': '%s',
                     'binary': '%s',
                     'bit': '%s',
                     'char': '%s',
                     'date': '%s',
                     'datetime': '%s',
                     'datetime2': '%s',
                     'datetimeoffset': '%s',
                     'decimal': '%s',
                     'float': '%s',
                     'image': '%s',
                     'int': '%s',
                     'money': '%s',
                     'nchar': '%s',
                     'ntext': '%s',
                     'numeric': '%s',
                     'nvarchar': '%s',
                     'real': '%s',
                     'smalldatetime': '%s',
                     'smallint': '%s',
                     'smallmoney': '%s',
                     'text': '%s',
                     'time': '%s',
                     'tinyint': '%s',
                     'varbinary': '%s',
                     'varchar': '%s',
                     'xml': '%s'}

        if data_type in templates:
            return templates[data_type]

        raise Exception('Unexpected data type %s.' % data_type)


# ----------------------------------------------------------------------------------------------------------------------
