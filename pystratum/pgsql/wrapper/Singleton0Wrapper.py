from pystratum.pgsql.wrapper.PgSqlWrapper import PgSqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class Singleton0Wrapper(PgSqlWrapper):
    """
    Wrapper method generator for stored procedures that are selecting 0 or 1 row with one column only.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_singleton0({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
