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
    """

    name = 'stratum'

    arguments = [
        {
            'name':        'config_file',
            'description': 'The audit configuration file',
            'required':    True
        },
        {
            'name':        'file_names',
            'description': 'Sources with stored routines',
            'list':        True
        }
    ]

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the actual Stratum program.
        """
        self.io = PyStratumStyle(self.input, self.output)

        command = self.get_application().find('constants')
        command.execute(self.input, self.output)

        command = self.get_application().find('loader')
        command.execute(self.input, self.output)

        command = self.get_application().find('wrapper')
        command.execute(self.input, self.output)

        self.io.writeln('')

# ----------------------------------------------------------------------------------------------------------------------
