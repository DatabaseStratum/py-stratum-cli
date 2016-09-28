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

    wrapper
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
        Executes wrapper command when PyStratumCommand is activated.
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

        wrapper = self.create_routine_wrapper_generator(rdbms)
        wrapper.main(config_file)

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_wrapper_generator(self, rdbms):
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
            return module.MySqlRoutineWrapperGenerator(self.output)

        if rdbms == 'mssql':
            module = locate('pystratum_mssql.MsSqlRoutineWrapperGenerator')
            return module.MsSqlRoutineWrapperGenerator(self.output)

        if rdbms == 'pgsql':
            module = locate('pystratum_pgsql.PgSqlRoutineWrapperGenerator')
            return module.PgSqlRoutineWrapperGenerator(self.output)

        raise Exception("Unknown RDBMS '{0!s}'.".format(rdbms))

# ----------------------------------------------------------------------------------------------------------------------
