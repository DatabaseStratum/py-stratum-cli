from typing import List, Optional

from pystratum_backend.RoutineLoaderWorker import RoutineLoaderWorker
from pystratum_backend.StratumStyle import StratumStyle


class VoidRoutineLoaderWorker(RoutineLoaderWorker):
    """
    Routine loader worker that does nothing.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumStyle):
        """
        Object constructor.

        :param io: The Output decorator.
        """
        self._io: StratumStyle = io

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, file_names: Optional[List[str]] = None) -> int:
        """
        Does the actual execution of the routine loader command for the backend. Returns 0 on success. Otherwise
        returns nonzero.

        :param list[str]|None file_names: The sources that must be loaded. If none all sources (if required) will
                                          loaded.

        :rtype: int
        """
        self._io.title('Loader')

        return 0

# ----------------------------------------------------------------------------------------------------------------------
