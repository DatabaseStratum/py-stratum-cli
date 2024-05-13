from unittest import TestCase

from cleo.testers.command_tester import CommandTester

from pystratum_cli import StratumApplication


class StratumApplicationNoneTest(TestCase):
    """
    Test with the none backend.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test_command_stratum(self) -> None:
        """
        Test stratum command with none backend.
        """
        application = StratumApplication()

        command = application.find('stratum')
        command_tester = CommandTester(command)
        status = command_tester.execute('test/etc/none.cfg')
        output = command_tester.io.fetch_output()

        self.assertEqual(0, status)
        self.assertEqual('', output)

    # ------------------------------------------------------------------------------------------------------------------
    def test_command_constants(self) -> None:
        """
        Test constants command with none backend.
        """
        application = StratumApplication()

        command = application.find('constants')
        command_tester = CommandTester(command)
        status = command_tester.execute('test/etc/none.cfg')
        output = command_tester.io.fetch_output()

        self.assertEqual(-1, status)
        self.assertIn('Constants', output)
        self.assertIn('ERROR', output)

    # ------------------------------------------------------------------------------------------------------------------
    def test_command_loader(self) -> None:
        """
        Test constants command with none backend.
        """
        application = StratumApplication()

        command = application.find('loader')
        command_tester = CommandTester(command)
        status = command_tester.execute('test/etc/none.cfg')
        output = command_tester.io.fetch_output()

        self.assertEqual(-1, status)
        self.assertIn('Loader', output)
        self.assertIn('ERROR', output)

    # ------------------------------------------------------------------------------------------------------------------
    def test_command_wrapper(self) -> None:
        """
        Test constants command with none backend.
        """
        application = StratumApplication()

        command = application.find('wrapper')
        command_tester = CommandTester(command)
        status = command_tester.execute('test/etc/none.cfg')
        output = command_tester.io.fetch_output()

        self.assertEqual(-1, status)
        self.assertIn('Wrapper', output)
        self.assertIn('ERROR', output)

# ----------------------------------------------------------------------------------------------------------------------
