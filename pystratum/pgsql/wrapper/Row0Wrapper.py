from pystratum.pgsql.wrapper.PgSqlWrapper import PgSqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class Row0Wrapper(PgSqlWrapper):
    """
    Wrapper method generator for stored procedures that are selecting 0 or 1 row.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_row0({0!s})'.format(self._generate_command(routine)))


# ----------------------------------------------------------------------------------------------------------------------
