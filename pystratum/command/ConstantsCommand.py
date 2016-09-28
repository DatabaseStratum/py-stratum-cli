"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import configparser
from pydoc import locate

from cleo import Command

from pystratum.style.PyStratumStyle import PyStratumStyle


class ConstantsCommand(Command):
    """
    Generates constants based on database IDs

    constants
        {config_file : The audit configuration file}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, i, o):
        self.input = i
        self.output = o

        return self.handle()

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes constants command when PyStratumCommand is activated.
        """
        self.output = PyStratumStyle(self.input, self.output)

        config_file = self.input.get_argument('config_file')
        self.run_command(config_file)

    # ------------------------------------------------------------------------------------------------------------------
    def run_command(self, config_file):
        """
        :param str config_file: The name of config file.
        """
        config = configparser.ConfigParser()

        config.read(config_file)

        rdbms = config.get('database', 'rdbms').lower()
        label_regex = config.get('constants', 'label_regex')

        constants = self.create_constants(rdbms)
        constants.main(config_file, label_regex)

    # ------------------------------------------------------------------------------------------------------------------
    def create_constants(self, rdbms):
        """
        Factory for creating a Constants objects (i.e. objects for creating constants based on column widths, and auto
        increment columns and labels).

        :param str rdbms: The target RDBMS (i.e. mysql, mssql or pgsql).

        :rtype: pystratum.Constants.Constants
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
