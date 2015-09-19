import os
from test.pgsql.StratumTestCase import StratumTestCase
from test.pgsql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class MagicConstantTest(StratumTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Test constant __ROUTINE__. Must return name of routine.
        """
        ret = DataLayer.tst_magic_constant01()
        self.assertEqual('tst_magic_constant01', ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Test constant __LINE__. Must return line number in the source code.
        """
        ret = DataLayer.tst_magic_constant02()
        self.assertEqual(13, int(ret))

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        Test constant __FILE__. Must return the filename of the source of the routine.
        """
        dir_cur_file = os.path.dirname(os.path.abspath(__file__))
        path = os.path.realpath(dir_cur_file + "/psql/tst_magic_constant03.psql")
        filename = os.path.realpath(path)
        ret = DataLayer.tst_magic_constant03()
        self.assertEqual(filename, ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test4(self):
        """
        Test constant __DIR__. Must return name of the folder where the source file of routine the is located.
        """
        dir_cur_file = os.path.dirname(os.path.abspath(__file__))
        dir_name = os.path.realpath(dir_cur_file + '/psql')
        ret = DataLayer.tst_magic_constant04()
        self.assertEqual(dir_name, ret)

# ----------------------------------------------------------------------------------------------------------------------
