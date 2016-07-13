from cleo import Application

from pystratum.command.PyStratumCommand import PyStratumCommand
from pystratum.command.ConstantsCommand import ConstantsCommand
from pystratum.command.LoaderCommand import LoaderCommand
from pystratum.command.WrapperCommand import WrapperCommand


class PyStratumApplication(Application):
    """
    The py-stratum application.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def get_default_commands(self):
        commands = Application.get_default_commands(self)

        self.add(PyStratumCommand())
        self.add(ConstantsCommand())
        self.add(LoaderCommand())
        self.add(WrapperCommand())

        return commands

# ----------------------------------------------------------------------------------------------------------------------
