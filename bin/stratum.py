#!/usr/bin/python3
import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/..'))

from lib.stratum.mysql.RoutineLoader import RoutineLoader

loader = RoutineLoader()
ret = loader.main(sys.argv[2])

exit(ret)
