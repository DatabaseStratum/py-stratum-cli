from pystratum.mysql.wrapper.MySqlWrapper import MySqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class Singleton1Wrapper(MySqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_singleton1({0!s})'.format(str(self._generate_command(routine))))


# ----------------------------------------------------------------------------------------------------------------------
