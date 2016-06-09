import abc

from pystratum.wrapper.Wrapper import Wrapper


# ----------------------------------------------------------------------------------------------------------------------
class PgSqlWrapper(Wrapper):
    """
    Parent class for wrapper method generators for stored functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def is_lob_parameter(self, parameters):
        """
        Returns True if one of the parameters is a BLOB or CLOB. Otherwise, returns False.

        :param list[dict[str,str]] parameters: The parameters of a stored routine.

        :rtype: bool
        """
        has_lob = False

        lookup = {'bigint':                      False,
                  'integer':                     False,
                  'bit':                         False,
                  'smallint':                    False,
                  'money':                       False,
                  'numeric':                     False,
                  'real':                        False,
                  'character':                   False,
                  'character varying':           False,
                  'timestamp without time zone': False,
                  'time without time zone':      False,
                  'date':                        False,
                  'boolean':                     False,

                  'bytea':                       True,
                  'text':                        True}

        if parameters:
            for parameter_info in parameters:
                if parameter_info['data_type'] in lookup:
                    has_lob = lookup[parameter_info['data_type']]
                else:
                    raise Exception("Unexpected date type '{0!s}'.".format(parameter_info['data_type']))

        return has_lob

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

        :param dict routine: Metadata of the stored routine.

        :rtype: str
        """
        parameters = ''
        placeholders = ''

        execute = 'select'

        i = 0
        l = 0
        for parameter in routine['parameters']:
            re_type = self._get_parameter_format_specifier(parameter)
            if parameters:
                parameters += ', '
                placeholders += ', '
            parameters += parameter['name']
            placeholders += re_type
            i += 1
            if not re_type == '?':
                l += 1

        if l == 0:
            line = '"{0!s} {1!s}()"'.format(execute, routine['routine_name'])
        elif l >= 1:
            line = '"{0!s} {1!s}({2!s})", {3!s}'.format(execute, routine['routine_name'], placeholders, parameters)
        else:
            raise Exception('Internal error.')

        return line

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_parameter_format_specifier(parameter):
        """
        Returns the appropriate format specifier for a parameter type.

        :param dict[str,str] parameter: The parameter metadata.

        :rtype: str
        """
        lookup = {'bigint':                      '%s::bigint',
                  'integer':                     '%s::int',
                  'bit':                         '%s::bit(4)',
                  'smallint':                    '%s::smallint',
                  'money':                       '%s::money',
                  'numeric':                     '%s::numeric',
                  'real':                        '%s::real',
                  'character':                   '%s::char',
                  'character varying':           '%s::varchar',
                  'timestamp without time zone': '%s::timestamp',
                  'time without time zone':      '%s::timestamp',
                  'boolean':                     '%s::bool',
                  'date':                        '%s::date',
                  'bytea':                       '%s::bytea',
                  'text':                        '%s::text'}

        if parameter['data_type'] in lookup:
            return lookup[parameter['data_type']]

        raise Exception('Unexpected data type {0!s}.'.format(parameter['data_type']))

# ---------------------------------------------------------------------------------------------------------------------
