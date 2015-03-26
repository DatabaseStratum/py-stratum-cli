from pystratum.mssql.wrapper.Wrapper import Wrapper


# ----------------------------------------------------------------------------------------------------------------------
class NoneWrapper(Wrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_none(%s)' % self._generate_command(routine))


# ----------------------------------------------------------------------------------------------------------------------
