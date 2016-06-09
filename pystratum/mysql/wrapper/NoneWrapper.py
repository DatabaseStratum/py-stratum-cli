from pystratum.mysql.wrapper.MySqlWrapper import MySqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class NoneWrapper(MySqlWrapper):
    """
    Wrapper method generator for stored procedures without any result set.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_none({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
