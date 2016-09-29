"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum.exception.ResultException import ResultException
from test.DataLayer import DataLayer
from test.StratumTestCase import StratumTestCase


class Singleton0Test(StratumTestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type singleton0 must return null.
        """
        from test.DataLayer import DataLayer
        ret = DataLayer.tst_test_singleton0a(0)
        self.assertIsNone(ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Stored routine with designation type singleton0 must return 1 value.
        """
        ret = DataLayer.tst_test_singleton0a(1)
        self.assertIsInstance(ret, (str, int, float))

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        An exception must be thrown when a stored routine with designation type singleton0 returns more than 1 values.
        """
        with self.assertRaises(ResultException):
            DataLayer.tst_test_singleton0a(2)

# ----------------------------------------------------------------------------------------------------------------------
