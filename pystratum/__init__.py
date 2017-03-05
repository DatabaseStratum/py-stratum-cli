"""
PyStratum
"""
from pystratum.application.PyStratumApplication import PyStratumApplication


def main():
    application = PyStratumApplication()
    ret = application.run()

    return ret
