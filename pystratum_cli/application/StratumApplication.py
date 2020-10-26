from typing import List

from cleo import Application, Command

from pystratum_cli.command.ConstantsCommand import ConstantsCommand
from pystratum_cli.command.RoutineLoaderCommand import RoutineLoaderCommand
from pystratum_cli.command.RoutineWrapperCommand import RoutineWrapperCommand
from pystratum_cli.command.StratumCommand import StratumCommand


class StratumApplication(Application):
    """
    The PyStratum application.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor
        """
        Application.__init__(self, 'pystratum', '1.0.4')

    # ------------------------------------------------------------------------------------------------------------------
    def get_default_commands(self) -> List[Command]:
        """
        Returns the default commands of this application.

        :rtype: list[Command]
        """
        commands = Application.get_default_commands(self)

        self.add(ConstantsCommand())
        self.add(RoutineLoaderCommand())
        self.add(StratumCommand())
        self.add(RoutineWrapperCommand())

        return commands

# ----------------------------------------------------------------------------------------------------------------------
