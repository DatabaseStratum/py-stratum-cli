#!/usr/bin/python3
import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/..'))

import pystratum

pystratum.main()
