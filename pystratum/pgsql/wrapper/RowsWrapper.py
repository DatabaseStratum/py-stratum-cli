from pystratum.pgsql.wrapper.PgSqlWrapper import PgSqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class RowsWrapper(PgSqlWrapper):
    """
    Wrapper method generator for stored procedures that are selecting 0, 1, or more rows.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_rows({0!s})'.format(self._generate_command(routine)))


# ----------------------------------------------------------------------------------------------------------------------
