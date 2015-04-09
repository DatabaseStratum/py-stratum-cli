from pystratum.mssql.wrapper.MsSqlWrapper import MsSqlWrapper
from pystratum.wrapper.RowsWithKeyWrapper import RowsWithKeyWrapper as BaseRowsWithKeyWrapper


# ----------------------------------------------------------------------------------------------------------------------
class RowsWithKeyWrapper(BaseRowsWithKeyWrapper, MsSqlWrapper):

    # ------------------------------------------------------------------------------------------------------------------
    def _write_execute_rows(self, routine):
        self._write_line('rows = StaticDataLayer.execute_rows(%s)' % self._generate_command(routine))


# ----------------------------------------------------------------------------------------------------------------------
