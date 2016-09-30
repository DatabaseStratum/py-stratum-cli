"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum.wrapper.LogWrapper import LogWrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlMultiWrapper(MySqlWrapper, LogWrapper):
    """
    Wrapper method generator for stored procedures with designation type multi.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_multi({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
