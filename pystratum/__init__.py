import argparse
from pystratum.mysql.RoutineLoader import RoutineLoader
from pystratum.mysql.RoutineWrapperGenerator import RoutineWrapperGenerator
from pystratum.mysql.Constants import Constants


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

    file_names = None
    if args.file_names:
        file_names = args.file_names

    if args.fast:
        # Fast mode: only load stored routines.
        loader = RoutineLoader()
        ret = loader.main(args.config[0], file_names)
        exit(ret)
    else:
        # Normal mode: create constants, config file, load routines, and create routine wrapper class.
        constants = Constants()
        ret = constants.main(args.config[0])
        if ret != 0:
            exit(ret)

        loader = RoutineLoader()
        ret = loader.main(args.config[0], file_names)
        if ret != 0:
            exit(ret)

        wrapper = RoutineWrapperGenerator()
        ret = wrapper.run(args.config[0])
        exit(ret)


# ----------------------------------------------------------------------------------------------------------------------
