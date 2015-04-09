from test.mssql.StratumTestCase import StratumTestCase
from test.mssql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class FunctionTest(StratumTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type function executes a stored function and return result.
        """
        ret = DataLayer.tst_test_function(2, 3)
        self.assertEqual(5, ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Stored routine with designation type function execute stored function and return result.
        """
        ret = DataLayer.tst_test_function(3, 4)
        self.assertNotEqual(5, ret)

# ----------------------------------------------------------------------------------------------------------------------
