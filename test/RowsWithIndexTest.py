from pprint import pprint
from test.DataLayer import DataLayer
from test.DataLayerTestCase import DataLayerTestCase


# ----------------------------------------------------------------------------------------------------------------------
class RowsWithIndexTest(DataLayerTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type rows_with_index must return multi dimensional array.
        """
        rows = DataLayer.tst_test_rows_with_index1(100)
        self.assertIsInstance(rows, dict)
        self.assertTrue('a' in rows)
        self.assertTrue('b' in rows['a'])
        self.assertNotEqual(0, len(rows['a']['b']))

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Stored routine with designation type rows_with_index must return empty array when no rwos are selected.
        """
        rows = DataLayer.tst_test_rows_with_index1(0)
        self.assertIsInstance(rows, dict)
        self.assertEqual(0, len(rows))

# ----------------------------------------------------------------------------------------------------------------------

