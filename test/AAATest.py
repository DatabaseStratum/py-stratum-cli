"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import unittest

from cleo import CommandTester
from pystratum.application.PyStratumApplication import PyStratumApplication


class AAATest(unittest.TestCase):
    """
    This test must run before all other tests because this test loads the stored routines.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type function executes a stored function and return result.
        """
        application = PyStratumApplication()
        command = application.find('stratum')
        command_tester = CommandTester(command)
        status = command_tester.execute([('command', command.get_name()),
                                         ('config_file', 'test/etc/stratum.cfg')])

        self.assertEqual(0, status)

# ----------------------------------------------------------------------------------------------------------------------
