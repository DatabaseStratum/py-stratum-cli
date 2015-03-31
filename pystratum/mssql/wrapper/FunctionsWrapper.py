from pystratum.mssql.wrapper.MsSqlWrapper import MsSqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class FunctionsWrapper(MsSqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    # select instead of call
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_singleton1(%s)' % self._generate_command(routine))


# ----------------------------------------------------------------------------------------------------------------------
