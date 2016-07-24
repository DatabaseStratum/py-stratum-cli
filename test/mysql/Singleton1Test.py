"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from mysql.connector import DataError
from test.mysql.StratumTestCase import StratumTestCase
from test.mysql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class Singleton1Test(StratumTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type singleton1 must return 1 value and 1 value only.
        """
        ret = DataLayer.tst_test_singleton1a(1)
        self.assertEqual(1, ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        An exception must be thrown when a stored routine with designation type singleton1 returns 0 values.
        @expectedException Exception
        """
        with self.assertRaises(DataError):
            DataLayer.tst_test_singleton1a(0)

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        An exception must be thrown when a stored routine with designation type singleton1 returns more than 1 values.
        @expectedException Exception
        """
        with self.assertRaises(DataError):
            DataLayer.tst_test_singleton1a(2)

# ----------------------------------------------------------------------------------------------------------------------
