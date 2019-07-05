"""
PyStratum
"""
from cleo import Command, Input, Output

from pystratum.style.PyStratumStyle import PyStratumStyle


class PyStratumCommand(Command):
    """
    Loads stored routines and generates a wrapper class

    stratum
        {config_file : The stratum configuration file}
        {file_names?* : Sources with stored routines}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, input_object: Input, output_object: Output) -> int:
        """
        Executes this command.
        """
        self.input = input_object
        self.output = output_object

        return self.handle()

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self) -> int:
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
