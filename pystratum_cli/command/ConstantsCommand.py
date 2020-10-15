from pystratum_cli.command.BaseCommand import BaseCommand


class ConstantsCommand(BaseCommand):
    """
    Generates constants based on database IDs.

    constants
        {config_file : The stratum configuration file}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self) -> int:
        """
        Executes constants command when StratumCommand is activated.
        """
        self._read_config_file(self.input)

        factory = self._create_backend_factory()
        worker = factory.create_constant_worker(self._config, self._io)

        if not worker:
            self._io.title('Constants')
            self._io.error('Constants command is not implemented by the backend')
            return -1

        return worker.execute()

# ----------------------------------------------------------------------------------------------------------------------
