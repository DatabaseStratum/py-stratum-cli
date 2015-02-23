from pystratum.mysql.wrapper.Wrapper import Wrapper


# ----------------------------------------------------------------------------------------------------------------------
class RowsWrapper(Wrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_rows(%s)' % self._generate_command(routine))


# ----------------------------------------------------------------------------------------------------------------------
