"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum.wrapper.Singleton1Wrapper import Singleton1Wrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlSingleton1Wrapper(MySqlWrapper, Singleton1Wrapper):
    """
    Wrapper method generator for stored procedures that are selecting 1 row with one column only.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line(
            'return StaticDataLayer.execute_sp_singleton1({0!s})'.format(str(self._generate_command(routine))))

# ----------------------------------------------------------------------------------------------------------------------
