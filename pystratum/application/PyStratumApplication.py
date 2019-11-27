"""
PyStratum
"""
from typing import List

from cleo import Application, Command

from pystratum.command.ConstantsCommand import ConstantsCommand
from pystratum.command.LoaderCommand import LoaderCommand
from pystratum.command.PyStratumCommand import PyStratumCommand
from pystratum.command.WrapperCommand import WrapperCommand


class PyStratumApplication(Application):
    """
    The PyStratum application.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor
        """
        Application.__init__(self, 'pystratum', '0.10.22')

    # ------------------------------------------------------------------------------------------------------------------
    def get_default_commands(self) -> List[Command]:
        """
        Returns the default commands of this application.

        :rtype: list[Command]
        """
        commands = Application.get_default_commands(self)

        self.add(ConstantsCommand())
        self.add(LoaderCommand())
        self.add(PyStratumCommand())
        self.add(WrapperCommand())

        return commands

# ----------------------------------------------------------------------------------------------------------------------
