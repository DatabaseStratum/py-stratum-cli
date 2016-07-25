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
    """

    name = 'constants'

    arguments = [
        {
            'name':        'config_file',
            'description': 'The audit configuration file',
            'required':    True
        }
    ]

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, inp, out):
        """
        Executes constants command when PyStratumCommand is activated.
        """
        self.io = PyStratumStyle(inp, out)

        config_file = inp.get_argument('config_file')
        ConstantsCommand.run_command(config_file)

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes constants command.
        """
        self.io = PyStratumStyle(self.input, self.output)

        config_file = self.argument('config_file')
        ConstantsCommand.run_command(config_file)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def run_command(config_file):
        """
        :param str config_file: The name of config file.
        """
        config = configparser.ConfigParser()

        config.read(config_file)

        rdbms = config.get('database', 'rdbms').lower()
        label_regex = config.get('constants', 'label_regex')

        constants = ConstantsCommand.create_constants(rdbms)
        constants.main(config_file, label_regex)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_constants(rdbms):
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
            return module.MySqlConstants()

        if rdbms == 'mssql':
            module = locate('pystratum_mssql.MsSqlConstants')
            return module.MsSqlConstants()

        if rdbms == 'pgsql':
            module = locate('pystratum_pgsql.PgSqlConstants')
            return module.PgSqlConstants()

        raise Exception("Unknown RDBMS '{0!s}'.".format(rdbms))

# ----------------------------------------------------------------------------------------------------------------------
