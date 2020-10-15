from pystratum_backend.ConstantWorker import ConstantWorker
from pystratum_backend.StratumStyle import StratumStyle


class VoidConstantWorker(ConstantWorker):
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
        Does the actual execution of the constant command for the backend. Returns 0 on success. Otherwise returns
        nonzero.

        :rtype: int
        """
        self._io.title('Constants')

        return 0

# ----------------------------------------------------------------------------------------------------------------------
