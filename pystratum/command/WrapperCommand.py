"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import configparser
from pydoc import locate

from cleo import Command

from pystratum.style.PyStratumStyle import PyStratumStyle


class WrapperCommand(Command):
    """
    Command for generating a class with wrapper methods for calling stored routines in a MySQL/MsSQL/PgSQL database
    """

    # ------------------------------------------------------------------------------------------------------------------
    name = 'wrapper'

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
        Executes wrapper command when PyStratumCommand is activated.
        """
        self.io = PyStratumStyle(inp, out)

        config_file = inp.get_argument('config_file')
        WrapperCommand.run_command(config_file)

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes wrapper command.
        """
        self.io = PyStratumStyle(self.input, self.output)

        config_file = self.argument('config_file')
        WrapperCommand.run_command(config_file)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def run_command(config_file):
        """
        :param str config_file: The name of config file.
        """
        config = configparser.ConfigParser()
        config.read(config_file)

        rdbms = config.get('database', 'rdbms').lower()

        wrapper = WrapperCommand.create_routine_wrapper_generator(rdbms)
        wrapper.run(config_file)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_routine_wrapper_generator(rdbms):
        """
        Factory for creating a Constants objects (i.e. objects for generating a class with wrapper methods for calling
        stored routines in a database).

        :param str rdbms: The target RDBMS (i.e. mysql, mssql or pgsql).

        :rtype: pystratum.RoutineWrapperGenerator.RoutineWrapperGenerator
        """
        # Note: We load modules and classes dynamically such that on the end user's system only the required modules
        #       and other dependencies for the targeted RDBMS must be installed (and required modules and other
        #       dependencies for the other RDBMSs are not required).

        if rdbms == 'mysql':
            module = locate('pystratum_mysql.MySqlRoutineWrapperGenerator')
            return module.MySqlRoutineWrapperGenerator()

        if rdbms == 'mssql':
            module = locate('pystratum_mssql.MsSqlRoutineWrapperGenerator')
            return module.MsSqlRoutineWrapperGenerator()

        if rdbms == 'pgsql':
            module = locate('pystratum_pgsql.PgSqlRoutineWrapperGenerator')
            return module.PgSqlRoutineWrapperGenerator()

        raise Exception("Unknown RDBMS '{0!s}'.".format(rdbms))

# ----------------------------------------------------------------------------------------------------------------------
