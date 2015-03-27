import argparse
import configparser

from pystratum.mysql.Constants import Constants as MySqlConstants
from pystratum.mysql.RoutineLoader import RoutineLoader as MySqlRoutineLoader
from pystratum.mysql.RoutineLoaderHelper import RoutineLoaderHelper as MySqlRoutineLoaderHelper
from pystratum.mysql.RoutineWrapperGenerator import RoutineWrapperGenerator as MySqlRoutineWrapperGenerator

from pystratum.mssql.Constants import Constants as MsSqlConstants
from pystratum.mssql.RoutineLoader import RoutineLoader as MsSqlRoutineLoader
from pystratum.mssql.RoutineLoaderHelper import RoutineLoaderHelper as MsSqlRoutineLoaderHelper
from pystratum.mssql.RoutineWrapperGenerator import RoutineWrapperGenerator as MsSqlRoutineWrapperGenerator


# ----------------------------------------------------------------------------------------------------------------------
def create_constants(rdbms: str):
    if rdbms == 'mysql':
        return MySqlConstants()

    if rdbms == 'mssql':
        return MsSqlConstants()

    raise Exception("Unknown RDBMS '%s'." % rdbms)


# ----------------------------------------------------------------------------------------------------------------------
def create_routine_loader(rdbms: str):
    if rdbms == 'mysql':
        return MySqlRoutineLoader()

    if rdbms == 'mssql':
        return MsSqlRoutineLoader()

    raise Exception("Unknown RDBMS '%s'." % rdbms)


# ----------------------------------------------------------------------------------------------------------------------
def create_routine_loader_helper(rdbms: str):
    if rdbms == 'mysql':
        return MySqlRoutineLoaderHelper()

    if rdbms == 'mssql':
        return MsSqlRoutineLoaderHelper()

    raise Exception("Unknown RDBMS '%s'." % rdbms)


# ----------------------------------------------------------------------------------------------------------------------
def create_routine_wrapper_generator(rdbms: str):
    if rdbms == 'mysql':
        return MySqlRoutineWrapperGenerator()

    if rdbms == 'mssql':
        return MsSqlRoutineWrapperGenerator()

    raise Exception("Unknown RDBMS '%s'." % rdbms)


# ----------------------------------------------------------------------------------------------------------------------
def main():
    """
    The main function of PyStratum. This function must eb used as entry point for the console script pystratum.
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
