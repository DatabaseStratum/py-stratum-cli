from pystratum.mssql.wrapper.MsSqlWrapper import MsSqlWrapper
from pystratum.wrapper.RowsWithIndexWrapper import RowsWithIndexWrapper as BaseRowsWithIndexWrapper


# ----------------------------------------------------------------------------------------------------------------------
class RowsWithIndexWrapper(BaseRowsWithIndexWrapper, MsSqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_execute_rows(self, routine):
        self._write_line('rows = StaticDataLayer.execute_rows(%s)' % self._generate_command(routine))

# ----------------------------------------------------------------------------------------------------------------------
