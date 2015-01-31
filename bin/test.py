import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/..'))

from lib.stratum.mysql.StaticDataLayer import StaticDataLayer

StaticDataLayer.config['user'] = 'test'
StaticDataLayer.config['password'] = 'test'
StaticDataLayer.config['database'] = 'test'
StaticDataLayer.config['host'] = 'localhost'
StaticDataLayer.connect()

print(StaticDataLayer.execute_sp_row0('call tst_test_row1a(%s)', 1))