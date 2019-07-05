"""
PyStratum
"""
from pystratum.application.PyStratumApplication import PyStratumApplication


def main() -> int:
    application = PyStratumApplication()
    ret = application.run()

    return ret
