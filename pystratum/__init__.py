import argparse
import configparser
from pydoc import locate


# ----------------------------------------------------------------------------------------------------------------------
def create_constants(rdbms: str):
    """
    Factory for creating a Constants objects (i.e. objects for creating constants based on column widths, and auto
    increment columns and labels).

    :param rdbms: The target RDBMS (i.e. mysql, mssql or pgsql).

    :rtype : pystratum.Constants.Constants
    """
    # Note: We load modules and classes dynamically such that on the end user's system only the required modules
    #       and other dependencies for the targeted RDBMS must be installed (and required modules and other
    #       dependencies for the other RDBMSs are not required).

    if rdbms == 'mysql':
        module = locate('pystratum.mysql.MySqlConstants')
        return module.MySqlConstants()

    if rdbms == 'mssql':
        module = locate('pystratum.mssql.MsSqlConstants')
        return module.MsSqlConstants()

    if rdbms == 'pgsql':
        module = locate('pystratum.pgsql.PgSqlConstants')
        return module.PgSqlConstants()

    raise Exception("Unknown RDBMS '{0!s}'.".format(rdbms))


# ----------------------------------------------------------------------------------------------------------------------
def create_routine_loader(rdbms):
    """
    Factory for creating a Routine Loader objects (i.e. objects for loading stored routines into a RDBMS instance from
    (pseudo) SQL files.

    :param str rdbms: The target RDBMS (i.e. mysql, mssql or pgsql).

    :rtype: pystratum.RoutineLoader.RoutineLoader
    """
    # Note: We load modules and classes dynamically such that on the end user's system only the required modules
    #       and other dependencies for the targeted RDBMS must be installed (and required modules and other
    #       dependencies for the other RDBMSs are not required).

    if rdbms == 'mysql':
        module = locate('pystratum.mysql.MySqlRoutineLoader')
        return module.MySqlRoutineLoader()

    if rdbms == 'mssql':
        module = locate('pystratum.mssql.MsSqlRoutineLoader')
        return module.MsSqlRoutineLoader()

    if rdbms == 'pgsql':
        module = locate('pystratum.pgsql.PgSqlRoutineLoader')
        return module.PgSqlRoutineLoader()

    raise Exception("Unknown RDBMS '{0!s}'.".format(rdbms))


# ----------------------------------------------------------------------------------------------------------------------
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
        module = locate('pystratum.mysql.MySqlRoutineWrapperGenerator')
        return module.MySqlRoutineWrapperGenerator()

    if rdbms == 'mssql':
        module = locate('pystratum.mssql.MsSqlRoutineWrapperGenerator')
        return module.MsSqlRoutineWrapperGenerator()

    if rdbms == 'pgsql':
        module = locate('pystratum.pgsql.PgSqlRoutineWrapperGenerator')
        return module.PgSqlRoutineWrapperGenerator()

    raise Exception("Unknown RDBMS '{0!s}'.".format(rdbms))


# ----------------------------------------------------------------------------------------------------------------------
def main():
    """
    The main function of PyStratum. This function must be used as entry point for the console script pystratum.
    """
    parser = argparse.ArgumentParser(description='Description')

    parser.add_argument(metavar='routine_file_name',
                        nargs='*',
                        dest='file_names',
                        help='the routine file names.')
    parser.add_argument('-c',
                        '--config',
                        metavar='<file_name>',
                        nargs=1, required=True,
                        dest='config',
                        help='Set path to the configuration filename.')
    parser.add_argument('-f',
                        '--fast',
                        action='store_true',
                        dest='fast',
                        help='Fast mode: only load stored routines.')

    args = parser.parse_args()
    config_filename = args.config[0]
    file_names = None
    if args.file_names:
        file_names = args.file_names

    config = configparser.ConfigParser()
    config.read(config_filename)

    rdbms = config.get('database', 'rdbms').lower()

    if args.fast:
        # Fast mode: only load stored routines.
        loader = create_routine_loader(rdbms)
        ret = loader.main(config_filename, file_names)
        exit(ret)
    else:
        # Normal mode: create constants, config file, load routines, and create routine wrapper class.
        constants = create_constants(rdbms)
        ret = constants.main(config_filename)
        if ret != 0:
            exit(ret)

        loader = create_routine_loader(rdbms)
        ret = loader.main(config_filename, file_names)
        if ret != 0:
            exit(ret)

        wrapper = create_routine_wrapper_generator(rdbms)
        ret = wrapper.run(config_filename)
        exit(ret)


# ----------------------------------------------------------------------------------------------------------------------
