from pystratum.mssql.wrapper.MsSqlWrapper import MsSqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class LogWrapper(MsSqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_log({0!s})'.format(self._generate_command(routine)))


# ----------------------------------------------------------------------------------------------------------------------
