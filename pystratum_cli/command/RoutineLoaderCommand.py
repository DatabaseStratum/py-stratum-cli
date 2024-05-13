from cleo.helpers import argument

from pystratum_cli.command.BaseCommand import BaseCommand


class RoutineLoaderCommand(BaseCommand):
    """
    Command for loading stored routines into a database instance from pseudo SQL files.
    """
    name = 'loader'
    description = 'Command for loading stored routines into a database instance from pseudo SQL files.'
    arguments = [argument(name='config_file', description='The stratum configuration file.'),
                 argument(name='file_names',  description='Sources with stored routines', optional=True, multiple=True)]

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self) -> int:
        """
        Executes constants command when StratumCommand is activated.
        """
        self._read_config_file()

        factory = self._create_backend_factory()
        worker = factory.create_routine_loader_worker(self._config, self._io)
        file_names = self.argument('file_names')

        if not worker:
            self._io.title('Loader')
            self._io.error('Loader command is not implemented by the backend')
            return -1

        return worker.execute(file_names)

# ----------------------------------------------------------------------------------------------------------------------
