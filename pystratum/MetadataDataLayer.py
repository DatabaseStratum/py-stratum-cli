"""
PyStratum
"""
import os
from typing import Optional

from pystratum.style.PyStratumStyle import PyStratumStyle


class MetadataDataLayer:
    """
    Data layer for retrieving metadata and loading stored routines.
    """
    io: Optional[PyStratumStyle] = None
    """
    The output decorator.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _log_query(query: str) -> None:
        """
        Logs the query on the console.

        :param str query: The query.
        """
        query = query.strip()

        if os.linesep in query:
            # Query is a multi line query
            MetadataDataLayer.io.log_very_verbose('Executing query:')
            MetadataDataLayer.io.log_very_verbose('<sql>{0}</sql>'.format(query))
        else:
            # Query is a single line query.
            MetadataDataLayer.io.log_very_verbose('Executing query: <sql>{0}</sql>'.format(query))

# ----------------------------------------------------------------------------------------------------------------------
