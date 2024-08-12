from cleo.application import Application
from cleo.io.io import IO
from cleo.io.outputs.output import Verbosity
from pystratum_backend.StratumIO import StratumIO

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
        Application.__init__(self, 'pystratum', '2.1.0')

        self.add(ConstantsCommand())
        self.add(RoutineLoaderCommand())
        self.add(StratumCommand())
        self.add(RoutineWrapperCommand())

    # ------------------------------------------------------------------------------------------------------------------
    def render_error(self, error: Exception, io: IO) -> None:
        if io.output.verbosity == Verbosity.NORMAL:
            my_io = StratumIO(io.input, io.output, io.error_output)
            lines = [error.__class__.__name__, str(error)]
            my_io.error(lines)
        else:
            Application.render_error(self, error, io)

# ----------------------------------------------------------------------------------------------------------------------
