from pystratum_backend.ConstantWorker import ConstantWorker
from pystratum_backend.StratumIO import StratumIO


class VoidConstantWorker(ConstantWorker):
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
        Does the actual execution of the constant command for the backend. Returns 0 on success. Otherwise returns
        nonzero.

        :rtype: int
        """
        self._io.title('Constants')

        return 0

# ----------------------------------------------------------------------------------------------------------------------
