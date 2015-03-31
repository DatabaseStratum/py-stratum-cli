from pystratum.mysql.wrapper.MySqlWrapper import MySqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class FunctionsWrapper(MySqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    # select instead of call
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_singleton1(%s)' % self._generate_command(routine))


# ----------------------------------------------------------------------------------------------------------------------
