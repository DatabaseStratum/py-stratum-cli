from pystratum.pgsql.wrapper.PgSqlWrapper import PgSqlWrapper
from pystratum.wrapper.RowsWithIndexWrapper import RowsWithIndexWrapper as BaseRowsWithIndexWrapper


# ----------------------------------------------------------------------------------------------------------------------
class RowsWithIndexWrapper(BaseRowsWithIndexWrapper, PgSqlWrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_execute_rows(self, routine):
        self._write_line('rows = StaticDataLayer.execute_sp_rows(%s)' % self._generate_command(routine))

# ----------------------------------------------------------------------------------------------------------------------
