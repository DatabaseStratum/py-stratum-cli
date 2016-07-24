"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc

from pystratum.wrapper.Wrapper import Wrapper


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlWrapper(Wrapper):
    """
    Parent class for wrapper method generators for stored procedures and functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def is_lob_parameter(self, parameters):
        """
        Returns True of one of the parameters is a BLOB or CLOB. Otherwise, returns False.

        :param parameters: The parameters of a stored routine.

        :rtype: bool:
        """
        has_blob = False

        lookup = {'bigint':         False,
                  'binary':         False,
                  'bit':            False,
                  'char':           False,
                  'date':           False,
                  'datetime':       False,
                  'datetime2':      False,
                  'datetimeoffset': False,
                  'decimal':        False,
                  'float':          False,
                  'geography':      True,
                  'geometry':       True,
                  'image':          True,
                  'int':            False,
                  'money':          False,
                  'nchar':          False,
                  'ntext':          True,
                  'numeric':        False,
                  'nvarchar':       False,
                  'real':           False,
                  'smalldatetime':  False,
                  'smallint':       False,
                  'smallmoney':     False,
                  'text':           True,
                  'time':           False,
                  'tinyint':        False,
                  'varbinary':      False,
                  'varchar':        False,
                  'xml':            True}

        if parameters:
            for parameter_info in parameters:
                if parameter_info['data_type'] in lookup:
                    has_blob = lookup[parameter_info['data_type']]
                else:
                    print("Unknown SQL type '{0!s}'.".format(parameter_info['data_type']))

        return has_blob

    # ------------------------------------------------------------------------------------------------------------------
    def _write_routine_method_without_lob(self, routine):

        self._write_line()
        self._write_separator()
        self._write_line('@staticmethod')
        self._write_line(
            'def {0!s}({1!s}):'.format(str(routine['routine_base_name']), str(self._get_wrapper_args(routine))))
        self._write_result_handler(routine)

        return self._code

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _write_result_handler(self, routine):
        """
        Generates code for calling the stored routine in the wrapper method.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _generate_command(self, routine):
        """
        Returns a SQL-statement for calling a stored routine.

        :param routine: Metadata of the stored routine.

        :rtype: str
        """
        if routine['parameters']:
            if routine['designation'] == 'function':
                sql = "'select [%s].[%s](%s)', %s"
            else:
                sql = "'exec [%s].[%s] %s', %s"

            parameters = ''
            placeholders = ''
            for parameter in routine['parameters']:
                if parameters:
                    parameters += ', '
                    placeholders += ', '
                parameters += parameter['name']
                placeholders += self._get_parameter_format_specifier(parameter['data_type'])

            ret = sql % (routine['schema_name'],
                         routine['routine_base_name'],  # routine_base_name
                         placeholders,
                         parameters)
        else:
            if routine['designation'] == 'function':
                sql = "'select [%s].[%s]()'"
            else:
                sql = "'exec [%s].[%s]'"

            ret = sql % (routine['schema_name'],
                         routine['routine_base_name'])

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_parameter_format_specifier(data_type):
        """
        Returns the appropriate format specifier for a parameter type.

        :param str data_type: The parameter type.

        :rtype: str
        """
        lookup = {'bigint':         '%s',
                  'binary':         '%s',
                  'bit':            '%s',
                  'char':           '%s',
                  'date':           '%s',
                  'datetime':       '%s',
                  'datetime2':      '%s',
                  'datetimeoffset': '%s',
                  'decimal':        '%s',
                  'float':          '%s',
                  'geography':      '%s',
                  'geometry':       '%s',
                  'image':          '%s',
                  'int':            '%s',
                  'money':          '%s',
                  'nchar':          '%s',
                  'ntext':          '%s',
                  'numeric':        '%s',
                  'nvarchar':       '%s',
                  'real':           '%s',
                  'smalldatetime':  '%s',
                  'smallint':       '%s',
                  'smallmoney':     '%s',
                  'text':           '%s',
                  'time':           '%s',
                  'tinyint':        '%s',
                  'varbinary':      '%s',
                  'varchar':        '%s',
                  'xml':            '%s'}

        if data_type in lookup:
            return '%s'

        raise Exception('Unexpected data type {0!s}.'.format(data_type))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_re_type(data_type):

        lob = '%s'

        templates = {'bigint':         '%s',
                     'binary':         '%s',
                     'bit':            '%s',
                     'char':           '%s',
                     'date':           '%s',
                     'datetime':       '%s',
                     'datetime2':      '%s',
                     'datetimeoffset': '%s',
                     'decimal':        '%s',
                     'float':          '%s',
                     'image':          lob,
                     'geography':      lob,
                     'geometry':       lob,
                     'int':            '%s',
                     'money':          '%s',
                     'nchar':          '%s',
                     'ntext':          lob,
                     'numeric':        '%s',
                     'nvarchar':       '%s',
                     'real':           '%s',
                     'smalldatetime':  '%s',
                     'smallint':       '%s',
                     'smallmoney':     '%s',
                     'text':           lob,
                     'time':           '%s',
                     'tinyint':        '%s',
                     'varbinary':      '%s',
                     'varchar':        '%s',
                     'xml':            lob}

        if data_type in templates:
            return templates[data_type]

        raise Exception('Unexpected data type {0!s}.'.format(data_type))

# ----------------------------------------------------------------------------------------------------------------------
