from pystratum.mssql.wrapper.MsSqlWrapper import MsSqlWrapper


# ----------------------------------------------------------------------------------------------------------------------
class TableWrapper(MsSqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_table({0!s})'.format(self._generate_command(routine)))


# ----------------------------------------------------------------------------------------------------------------------
