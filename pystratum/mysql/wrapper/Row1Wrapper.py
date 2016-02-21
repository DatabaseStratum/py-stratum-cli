from pystratum.mysql.wrapper.MySqlWrapper import MySqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class Row1Wrapper(MySqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_row1({0!s})'.format(self._generate_command(routine)))


# ----------------------------------------------------------------------------------------------------------------------
