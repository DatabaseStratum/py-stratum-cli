"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum.application.PyStratumApplication import PyStratumApplication


def main():
    application = PyStratumApplication()
    ret = application.run()

    return ret
