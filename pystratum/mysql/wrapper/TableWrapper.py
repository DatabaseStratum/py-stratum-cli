from pystratum.mysql.wrapper.MySqlWrapper import MySqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class TableWrapper(MySqlWrapper):
    """
    Wrapper method generator for printing the result set of stored procedures in a table format.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_table({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
