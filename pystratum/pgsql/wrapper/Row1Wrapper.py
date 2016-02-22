from pystratum.pgsql.wrapper.PgSqlWrapper import PgSqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class Row1Wrapper(PgSqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_row1({0!s})'.format(self._generate_command(routine)))


# ----------------------------------------------------------------------------------------------------------------------
