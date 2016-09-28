"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc

from pystratum.wrapper.Wrapper import Wrapper


class RowsWithKeyWrapper(Wrapper):
    """
    Parent class wrapper wrapper method generator for stored procedures whose result set must be returned using tree
    structure using a combination of unique columns.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _get_docstring_return_type(self):
        """
        Returns the return type of the wrapper methods the be used in the docstring.

        :rtype: str
        """
        return 'dict'

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _write_execute_rows(self, routine):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        """
        Generates code for calling the stored routine in the wrapper method.
        """
        self._write_line('ret = {}')
        self._write_execute_rows(routine)
        self._write_line('for row in rows:')

        num_of_dict = len(routine['columns'])

        i = 0
        while i < num_of_dict:
            value = "row['{0!s}']".format(routine['columns'][i])

            stack = ''
            j = 0
            while j < i:
                stack += "[row['{0!s}']]".format(routine['columns'][j])
                j += 1
            line = 'if {0!s} in ret{1!s}:'.format(value, stack)
            self._write_line(line)
            i += 1

        line = "raise Exception('Duplicate key for %s.' % str(({0!s})))". \
            format(", ".join(["row['{0!s}']".format(column_name) for column_name in routine['columns']]))

        self._write_line(line)
        self._indent_level_down()

        i = num_of_dict
        while i > 0:
            self._write_line('else:')

            part1 = ''
            j = 0
            while j < i - 1:
                part1 += "[row['{0!s}']]".format(routine['columns'][j])
                j += 1
            part1 += "[row['{0!s}']]".format(routine['columns'][j])

            part2 = ''
            j = i - 1
            while j < num_of_dict:
                if j + 1 != i:
                    part2 += "{{row['{0!s}']: ".format(routine['columns'][j])
                j += 1
            part2 += "row" + ('}' * (num_of_dict - i))

            line = "ret{0!s} = {1!s}".format(part1, part2)
            self._write_line(line)
            self._indent_level_down()
            if i > 1:
                self._indent_level_down()
            i -= 1

        self._write_line()
        self._write_line('return ret')

# ----------------------------------------------------------------------------------------------------------------------
