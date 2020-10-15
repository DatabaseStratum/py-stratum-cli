import os
from configparser import ConfigParser

from cleo import Command, Input, Output
from pystratum_backend.Backend import Backend
from pystratum_backend.StratumStyle import StratumStyle


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

        :type: ConfigParser 
        """

        self._io = None
        """
        The Output decorator.

        :type: StratumStyle|None 
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
    def _read_config_file(self, input_object: Input) -> None:
        """
        Reads the PyStratum configuration file.

        :rtype: ConfigParser
        """
        config_filename = input_object.get_argument('config_file')
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
    def execute(self, input_object: Input, output_object: Output) -> int:
        """
        Executes this command.

        :param input_object:  The input object.
        :param output_object: The output object.
        """
        self.input = input_object
        self.output = output_object

        self._io = StratumStyle(input_object, output_object)

        return self.handle()

# ----------------------------------------------------------------------------------------------------------------------
