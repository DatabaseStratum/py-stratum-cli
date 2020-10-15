from pystratum_backend.RoutineWrapperGeneratorWorker import RoutineWrapperGeneratorWorker
from pystratum_backend.StratumStyle import StratumStyle


class VoidRoutineWrapperGeneratorWorker(RoutineWrapperGeneratorWorker):
    """
    Constant worker that does nothing.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumStyle):
        """
        Object constructor.

        :param io: The Output decorator.
        """
        self._io: StratumStyle = io

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self) -> int:
        """
        Does the actual execution of the routine wrapper generator command for the backend. Returns 0 on success.
        Otherwise returns nonzero.

        :rtype: int
        """
        self._io.title('Wrapper')

        return 0

# ----------------------------------------------------------------------------------------------------------------------
