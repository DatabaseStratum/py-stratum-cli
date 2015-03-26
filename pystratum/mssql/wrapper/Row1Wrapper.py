from pystratum.mssql.wrapper.Wrapper import Wrapper


# ----------------------------------------------------------------------------------------------------------------------
class Row1Wrapper(Wrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_row1(%s)' % self._generate_command(routine))


# ----------------------------------------------------------------------------------------------------------------------
