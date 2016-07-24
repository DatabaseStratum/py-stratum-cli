"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import OutputFormatterStyle
from cleo.styles import CleoStyle


class PyStratumStyle(CleoStyle):
    """
    Output style for py-stratum.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, input, output):
        """
        Object constructor.

        :param cleo.inputs.input.Input input: The input object.
        :param cleo.outputs.output.Output output: The output object.
        """
        CleoStyle.__init__(self, input, output)

        # Create style notes.
        style = OutputFormatterStyle('yellow', None, ['bold'])
        output.get_formatter().set_style('note', style)

        # Create style for database objects.
        style = OutputFormatterStyle('green', None, ['bold'])
        output.get_formatter().set_style('dbo', style)

        # Create style for file and directory names.
        style = OutputFormatterStyle('white', None, ['bold'])
        output.get_formatter().set_style('fso', style)

        # Create style for SQL statements.
        style = OutputFormatterStyle('magenta', None, ['bold'])
        output.get_formatter().set_style('sql', style)

# ----------------------------------------------------------------------------------------------------------------------
