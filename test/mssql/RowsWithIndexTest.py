from test.mssql.StratumTestCase import StratumTestCase
from test.mssql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class RowsWithIndexTest(StratumTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type rows_with_index must return multi dimensional array.
        """
        rows = DataLayer.tst_test_rows_with_index1(100)
        self.assertIsInstance(rows, dict)
        self.assertIn('a', rows)
        self.assertIn('b', rows['a'])
        self.assertIsInstance(rows['a']['b'], list)
        self.assertEqual(3, len(rows['a']['b']))

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Stored routine with designation type rows_with_index must return empty array when no rwos are selected.
        """
        rows = DataLayer.tst_test_rows_with_index1(0)
        self.assertIsInstance(rows, dict)
        self.assertEqual(0, len(rows))

# ----------------------------------------------------------------------------------------------------------------------

