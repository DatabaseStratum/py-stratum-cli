"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import configparser
from pydoc import locate

from cleo import Command

from pystratum.style.PyStratumStyle import PyStratumStyle


class LoaderCommand(Command):
    """
    Command for loading stored routines into a MySQL/MsSQL/PgSQL instance from pseudo SQL files
    """

    name = 'loader'

    arguments = [
        {
            'name':        'config_file',
            'description': 'The audit configuration file',
            'required':    True
        },
        {
            'name':        'file_names',
            'description': 'Sources with stored routines',
            'list':        True
        }
    ]

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes loader command.
        """
        self.output = PyStratumStyle(self.input, self.output)

        config_file = self.argument('config_file')
        sources = self.argument('file_names')

        status = LoaderCommand.run_command(config_file, sources)

        return status

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def run_command(config_file, sources):
        """
        :param str config_file: The name of config file.
        :param list sources: The list with source files.
        """
        config = configparser.ConfigParser()
        config.read(config_file)

        rdbms = config.get('database', 'rdbms').lower()

        loader = LoaderCommand.create_routine_loader(rdbms)
        status = loader.main(config_file, sources)

        return status

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_routine_loader(rdbms):
        """
        Factory for creating a Routine Loader objects (i.e. objects for loading stored routines into a RDBMS instance
        from (pseudo) SQL files.

        :param str rdbms: The target RDBMS (i.e. mysql, mssql or pgsql).

        :rtype: pystratum.RoutineLoader.RoutineLoader
        """
        # Note: We load modules and classes dynamically such that on the end user's system only the required modules
        #       and other dependencies for the targeted RDBMS must be installed (and required modules and other
        #       dependencies for the other RDBMSs are not required).

        if rdbms == 'mysql':
            module = locate('pystratum_mysql.MySqlRoutineLoader')
            return module.MySqlRoutineLoader()

        if rdbms == 'mssql':
            module = locate('pystratum_mssql.MsSqlRoutineLoader')
            return module.MsSqlRoutineLoader()

        if rdbms == 'pgsql':
            module = locate('pystratum_pgsql.PgSqlRoutineLoader')
            return module.PgSqlRoutineLoader()

        raise Exception("Unknown RDBMS '{0!s}'.".format(rdbms))

# ----------------------------------------------------------------------------------------------------------------------
