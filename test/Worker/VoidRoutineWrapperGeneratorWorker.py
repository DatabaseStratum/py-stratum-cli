from pystratum_backend.RoutineWrapperGeneratorWorker import RoutineWrapperGeneratorWorker
from pystratum_backend.StratumIO import StratumIO


class VoidRoutineWrapperGeneratorWorker(RoutineWrapperGeneratorWorker):
    """
    Constant worker that does nothing.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumIO):
        """
        Object constructor.

        :param io: The Output decorator.
        """
        self._io: StratumIO = io

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self) -> int:
        """
        Does the actual execution of the routine wrapper generator command for the backend. Returns 0 on success.
        Otherwise, returns nonzero.
        """
        self._io.title('Wrapper')

        return 0

# ----------------------------------------------------------------------------------------------------------------------
