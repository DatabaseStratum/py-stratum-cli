"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class Row1Wrapper(MySqlWrapper):
    """
    Wrapper method generator for stored procedures that are selecting 1 row.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_row1({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
