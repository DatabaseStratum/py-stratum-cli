import os
from configparser import ConfigParser

from cleo.commands.command import Command
from cleo.io.io import IO
from pystratum_backend.Backend import Backend
from pystratum_backend.StratumIO import StratumIO


class BaseCommand(Command):
    """
    Base command for other commands of PyStratum.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        super().__init__()

        self._config = ConfigParser()
        """
        The configuration object.
        """

        self._io: StratumIO | None = None
        """
        The Output decorator.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _create_backend_factory(self) -> Backend:
        """
        Creates the PyStratum Style object.
        """
        class_name = self._config['stratum']['backend']

        parts = class_name.split('.')
        module_name = ".".join(parts[:-1])
        module = __import__(module_name)
        for comp in parts[1:]:
            module = getattr(module, comp)

        return module()

    # ------------------------------------------------------------------------------------------------------------------
    def _read_config_file(self) -> None:
        """
        Reads the PyStratum configuration file.

        :rtype: ConfigParser
        """
        config_filename = self.argument('config_file')
        self._config.read(config_filename)

        if 'database' in self._config and 'supplement' in self._config['database']:
            path = os.path.join(os.path.dirname(config_filename), self._config.get('database', 'supplement'))
            config_supplement = ConfigParser()
            config_supplement.read(path)

            if 'database' in config_supplement:
                options = config_supplement.options('database')
                for option in options:
                    self._config['database'][option] = config_supplement['database'][option]

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, io: IO) -> int:
        """
        Executes this command.

        :param io: The input/output object.
        """
        self._io = StratumIO(io.input, io.output, io.error_output)

        return self.handle()

# ----------------------------------------------------------------------------------------------------------------------
