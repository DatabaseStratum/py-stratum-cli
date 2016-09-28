"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import Command

from pystratum.style.PyStratumStyle import PyStratumStyle


class PyStratumCommand(Command):
    """
    Loads stored routines and generates a wrapper class

    stratum
        {config_file : The audit configuration file}
        {file_names?* : Sources with stored routines}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, i, o):
        self.input = i
        self.output = o

        return self.handle()

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the actual Stratum program.
        """
        self.output = PyStratumStyle(self.input, self.output)

        command = self.get_application().find('constants')
        ret = command.execute(self.input, self.output)
        if ret:
            return ret

        command = self.get_application().find('loader')
        ret = command.execute(self.input, self.output)
        if ret:
            return ret

        command = self.get_application().find('wrapper')
        ret = command.execute(self.input, self.output)

        self.output.writeln('')

        return ret

# ----------------------------------------------------------------------------------------------------------------------
