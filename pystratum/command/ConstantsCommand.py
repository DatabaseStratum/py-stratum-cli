"""
PyStratum
"""
import configparser
from pydoc import locate

from cleo import Command, Input, Output
from pystratum.Constants import Constants

from pystratum.style.PyStratumStyle import PyStratumStyle


class ConstantsCommand(Command):
    """
    Generates constants based on database IDs

    constants
        {config_file : The audit configuration file}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, input_object: Input, output_object: Output) -> int:
        """
        Executes this command.
        """
        self.input = input_object
        self.output = output_object

        return self.handle()

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self) -> int:
        """
        Executes constants command when PyStratumCommand is activated.
        """
        self.output = PyStratumStyle(self.input, self.output)

        config_file = self.input.get_argument('config_file')

        return self.run_command(config_file)

    # ------------------------------------------------------------------------------------------------------------------
    def run_command(self, config_file: str) -> int:
        """
        :param str config_file: The name of config file.
        """
        config = configparser.ConfigParser()

        config.read(config_file)

        rdbms = config.get('database', 'rdbms').lower()
        label_regex = config.get('constants', 'label_regex')

        constants = self.create_constants(rdbms)
        constants.main(config_file, label_regex)

        return 0

    # ------------------------------------------------------------------------------------------------------------------
    def create_constants(self, rdbms: str) -> Constants:
        """
        Factory for creating a Constants objects (i.e. objects for creating constants based on column widths, and auto
        increment columns and labels).

        :param str rdbms: The target RDBMS (i.e. mysql, mssql or pgsql).

        :rtype: Constants
        """
        # Note: We load modules and classes dynamically such that on the end user's system only the required modules
        #       and other dependencies for the targeted RDBMS must be installed (and required modules and other
        #       dependencies for the other RDBMSs are not required).

        if rdbms == 'mysql':
            module = locate('pystratum_mysql.MySqlConstants')
            return module.MySqlConstants(self.output)

        if rdbms == 'mssql':
            module = locate('pystratum_mssql.MsSqlConstants')
            return module.MsSqlConstants(self.output)

        if rdbms == 'pgsql':
            module = locate('pystratum_pgsql.PgSqlConstants')
            return module.PgSqlConstants(self.output)

        raise Exception("Unknown RDBMS '{0!s}'.".format(rdbms))

# ----------------------------------------------------------------------------------------------------------------------
