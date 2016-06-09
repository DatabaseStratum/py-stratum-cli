from pystratum.pgsql.wrapper.PgSqlWrapper import PgSqlWrapper
from pystratum.wrapper.RowsWithKeyWrapper import RowsWithKeyWrapper as BaseRowsWithKeyWrapper


# ----------------------------------------------------------------------------------------------------------------------
class RowsWithKeyWrapper(BaseRowsWithKeyWrapper, PgSqlWrapper):
    """
    Wrapper method generator for stored procedures whose result set must be returned using tree structure using a
    combination of unique columns.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_execute_rows(self, routine):
        self._write_line('rows = StaticDataLayer.execute_sp_rows({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
