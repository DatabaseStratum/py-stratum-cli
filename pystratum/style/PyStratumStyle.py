"""
PyStratum
"""
from typing import List, Union

from cleo import Output, Input
from cleo.styles import CleoStyle


class PyStratumStyle(CleoStyle):
    """
    Output style for py-stratum.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, input_object: Input, output_object: Output):
        """
        Object constructor.

        :param Input input_object: The input object.
        :param Output output_object: The output object.
        """
        CleoStyle.__init__(self, input_object, output_object)

        # Create style notes.
        output_object.get_formatter().add_style('note', 'yellow', None, ['bold'])

        # Create style for database objects.
        output_object.get_formatter().add_style('dbo', 'green', None, ['bold'])

        # Create style for file and directory names.
        output_object.get_formatter().add_style('fso', 'white', None, ['bold'])

        # Create style for SQL statements.
        output_object.get_formatter().add_style('sql', 'magenta', None, ['bold'])

    # ------------------------------------------------------------------------------------------------------------------
    def warning(self, message: Union[str, List[str]]) -> None:
        self.block(message, 'WARNING', 'fg=white;bg=red', padding=True)

    # ------------------------------------------------------------------------------------------------------------------
    def text(self, message: Union[str, List[str]]) -> None:
        if isinstance(message, list):
            messages = message
        else:
            messages = [message]

        for line in messages:
            self.writeln(' {0}'.format(line))

    # ------------------------------------------------------------------------------------------------------------------
    def log_verbose(self, message: Union[str, List[str]]) -> None:
        """
        Logs a message only when logging level is verbose.

        :param str|list[str] message: The message.
        """
        if self.get_verbosity() >= Output.VERBOSITY_VERBOSE:
            self.writeln(message)

    # ------------------------------------------------------------------------------------------------------------------
    def log_very_verbose(self, message: Union[str, List[str]]) -> None:
        """
        Logs a message only when logging level is very verbose.

        :param str|list[str] message: The message.
        """
        if self.get_verbosity() >= Output.VERBOSITY_VERY_VERBOSE:
            self.writeln(message)

# ----------------------------------------------------------------------------------------------------------------------
