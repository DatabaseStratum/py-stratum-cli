from pystratum.mysql.wrapper.MySqlWrapper import MySqlWrapper
from pystratum.wrapper.RowsWithKeyWrapper import RowsWithKeyWrapper as BaseRowsWithKeyWrapper


# ----------------------------------------------------------------------------------------------------------------------
class RowsWithKeyWrapper(BaseRowsWithKeyWrapper, MySqlWrapper):

    # ------------------------------------------------------------------------------------------------------------------
    def _write_execute_rows(self, routine):
        self._write_line('rows = StaticDataLayer.execute_sp_rows(%s)' % self._generate_command(routine))


# ----------------------------------------------------------------------------------------------------------------------
