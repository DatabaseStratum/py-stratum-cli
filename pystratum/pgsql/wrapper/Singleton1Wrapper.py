from pystratum.pgsql.wrapper.PgSqlWrapper import PgSqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class Singleton1Wrapper(PgSqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_singleton1({0!s})'.format(str(self._generate_command(routine))))


# ----------------------------------------------------------------------------------------------------------------------
