from configparser import ConfigParser
import os


# ----------------------------------------------------------------------------------------------------------------------
class Connection:
    """
    Parent class for RDBMS connections.
    """
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_option(config, supplement, section, option, fallback=None):
        """
        Reads an option for a configuration file.

        :param ConfigParser config: The main config file.
        :param ConfigParser supplement: The supplement config file.
        :param str section: The name of the section op the option.
        :param str option: The name of the option.
        :param str fallback: The fallback value of the option if it is not set in either configuration files.
        :rtype: str
        :raise KeyError:
        """
        if supplement:
            return_value = supplement.get(section, option, fallback=config.get(section, option, fallback=fallback))
        else:
            return_value = config.get(section, option, fallback=fallback)

        if fallback is None and return_value is None:
            raise KeyError("Option '{0!s}' is not found in section '{1!s}'.".format(option, section))

        return return_value

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _read_configuration(config_filename):
        """
        Checks the supplement file.

        :param str config_filename: The path of main config file
        :rtype: (ConfigParser,ConfigParser)
        """
        config = ConfigParser()
        config.read(config_filename)

        if 'supplement' in config['database']:
            path = os.path.dirname(config_filename) + '/' + config.get('database', 'supplement')
            config_supplement = ConfigParser()
            config_supplement.read(path)
        else:
            config_supplement = None

        return config, config_supplement

# ----------------------------------------------------------------------------------------------------------------------
