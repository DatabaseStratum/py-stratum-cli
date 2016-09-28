"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import os


class MetadataDataLayer:
    """
    Data layer for retrieving metadata and loading stored routines.
    """
    io = None
    """
    The output decorator.

    :type: pystratum.style.PyStratumStyle.PyStratumStyle|None
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _log_query(query):
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
