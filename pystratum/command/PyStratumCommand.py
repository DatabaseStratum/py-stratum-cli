from cleo import Command

from pystratum.style.PyStratumStyle import PyStratumStyle


class PyStratumCommand(Command):
    """
    Loads stored routines and generates a wrapper class.

    stratum
        {config_file? : The audit configuration file}
        {sources?* : Sources with stored routines}
    """

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
