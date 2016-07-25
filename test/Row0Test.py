"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from mysql.connector import DataError

from test import DataLayer
from test import StratumTestCase


class Row0Test(StratumTestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type row0 must return null.
        """
        ret = DataLayer.tst_test_row0a(0)
        self.assertIsNone(ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Stored routine with designation type row0 must return 1 row.
        """
        ret = DataLayer.tst_test_row0a(1)
        self.assertIsInstance(ret, dict)

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        An exception must be thrown when a stored routine with designation type row0 returns more than 1 rows.
        @expectedException Exception
        """
        with self.assertRaises(DataError):
            DataLayer.tst_test_row0a(2)

# ----------------------------------------------------------------------------------------------------------------------
