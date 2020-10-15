from pystratum_cli.command.BaseCommand import BaseCommand


class RoutineLoaderCommand(BaseCommand):
    """
    Command for loading stored routines into a database instance from pseudo SQL files.

    loader
        {config_file : The audit configuration file}
        {file_names?* : Sources with stored routines}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self) -> int:
        """
        Executes constants command when StratumCommand is activated.
        """
        self._read_config_file(self.input)

        factory = self._create_backend_factory()
        worker = factory.create_routine_loader_worker(self._config, self._io)
        file_names = self.input.get_argument('file_names')

        if not worker:
            self._io.title('Loader')
            self._io.error('Loader command is not implemented by the backend')
            return -1

        return worker.execute(file_names)

# ----------------------------------------------------------------------------------------------------------------------
