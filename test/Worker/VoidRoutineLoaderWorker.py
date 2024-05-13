from typing import List, Optional

from pystratum_backend.RoutineLoaderWorker import RoutineLoaderWorker
from pystratum_backend.StratumIO import StratumIO


class VoidRoutineLoaderWorker(RoutineLoaderWorker):
    """
    Routine loader worker that does nothing.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumIO):
        """
        Object constructor.

        :param io: The Output decorator.
        """
        self._io: StratumIO = io

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, file_names: Optional[List[str]] = None) -> int:
        """
        Does the actual execution of the routine loader command for the backend. Returns 0 on success. Otherwise,
        returns nonzero.

        :param file_names: The sources that must be loaded. If None all sources (if required) will be loaded.
        """
        self._io.title('Loader')

        return 0

# ----------------------------------------------------------------------------------------------------------------------
