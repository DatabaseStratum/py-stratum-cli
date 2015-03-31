from pystratum.mysql.wrapper.MySqlWrapper import MySqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class RowsWithKeyWrapper(MySqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('ret = {}')
        self._write_line('rows = StaticDataLayer.execute_sp_rows(%s)' % self._generate_command(routine))
        self._write_line('for row in rows:')

        num_of_dict = len(routine['columns'])

        i = 0
        while i < num_of_dict:
            value = "row['%s']" % routine['columns'][i]

            stack = ''
            j = 0
            while j < i:
                stack += "[row['%s']]" % routine['columns'][j]
                j += 1
            line = 'if %s in ret%s:' % (value, stack)
            self._write_line(line)
            i += 1

        self._write_line('pass')
        self._indent_level_down()

        i = num_of_dict
        while i > 0:
            self._write_line('else:')

            part1 = ''
            j = 0
            while j < i - 1:
                part1 += "[row['%s']]" % routine['columns'][j]
                j += 1

            part2 = ''
            j = i - 1
            while j < num_of_dict:
                part2 += "{row['%s']: " % routine['columns'][j]
                j += 1
            part2 += 'row' + ('}' * (num_of_dict - i + 1))

            line = "ret%s.update(%s)" % (part1, part2)
            self._write_line(line)
            self._indent_level_down()
            if i > 1:
                self._indent_level_down()
            i -= 1

        self._write_line()
        self._write_line('return ret')


# ----------------------------------------------------------------------------------------------------------------------
