from pystratum.mysql.wrapper.MySqlWrapper import MySqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class FunctionsWrapper(MySqlWrapper):
    """
    Wrapper method generator for stored functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_singleton1({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
