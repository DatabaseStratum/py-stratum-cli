from test.mssql.StratumTestCase import StratumTestCase
from test.mssql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class RowsTest(StratumTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type rows must return an empty array when no rows are selected.
        """
        ret = DataLayer.tst_test_rows(0)
        self.assertIsInstance(ret, list)
        self.assertEqual(0, len(ret))

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Stored routine with designation type rows must return an array with 1 row when only 1 row is selected.
        """
        ret = DataLayer.tst_test_rows(1)
        self.assertIsInstance(ret, list)
        self.assertEqual(1, len(ret))

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        Stored routine with designation type rows must return an array with 3 rows when 3 rows are selected.
        """
        ret = DataLayer.tst_test_rows(3)
        self.assertIsInstance(ret, list)
        self.assertEqual(3, len(ret))

# ----------------------------------------------------------------------------------------------------------------------
