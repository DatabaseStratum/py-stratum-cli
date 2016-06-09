from pystratum.pgsql.wrapper.PgSqlWrapper import PgSqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class FunctionsWrapper(PgSqlWrapper):
    """
    Wrapper method generator for stored functions.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_singleton1({0!s})'.format(self._generate_command(routine)))


# ----------------------------------------------------------------------------------------------------------------------
