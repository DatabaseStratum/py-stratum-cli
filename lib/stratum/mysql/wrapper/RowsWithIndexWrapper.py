from lib.stratum.mysql.wrapper.Wrapper import Wrapper


# ----------------------------------------------------------------------------------------------------------------------
class RowsWithIndexWrapper(Wrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('rows = StaticDataLayer.execute_sp_rows(%s)' % self._generate_command(routine))
        self._write_line('if rows:')
        i = 0
        line = 'return '
        num_of_dict = len(routine['columns'])
        for column in routine['columns']:
            line += "{rows[0]['%s']: " % column
            i += 1
        line += 'rows' + ('}' * num_of_dict)
        self._write_line(line)

        self._indent_level_down()

        self._write_line('else:')
        self._write_line('return {}')

# ----------------------------------------------------------------------------------------------------------------------
