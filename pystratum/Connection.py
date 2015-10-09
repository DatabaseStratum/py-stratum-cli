import configparser
import os

# ----------------------------------------------------------------------------------------------------------------------
class Connection:
    """
    Base class for connections and configurations files.
    """
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_option(config, supplement, section, option, fallback=None):
        """
        Reads a option for a configuration file.
        :param configparser.ConfigParser config: The main config file.
        :param configparser.ConfigParser supplement: The supplement config file.
        :param str section: The name of the section op the option.
        :param str option: The name of the option.
        :param mixed fallback: The fallback value of the option if it is not set in either configuration files.
        :rtype: str
        :raise KeyError:
        """
        if supplement:
            return_value = supplement.get(section, option,
                                          fallback=config.get(section, option, fallback=fallback))
        else:
            return_value = config.get(section, option, fallback=fallback)

        if fallback is not None and return_value is None:
            raise KeyError("The option '%s' is not found in section '%s'." % (option, section))

        return return_value

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _read_configuration(config_filename):
        """
        Checks the supplement file.
        :param str config_filename: The path of main config file
        :rtype: configparser.ConfigParser or None
        """
        config = configparser.ConfigParser()
        config.read(config_filename)

        if 'supplement' in config['database']:
            path = os.path.dirname(config_filename) + '/' + config.get('database', 'supplement')
            config_supplement = configparser.ConfigParser()
            config_supplement.read(path)
        else:
            config_supplement = None

        return config, config_supplement


# ----------------------------------------------------------------------------------------------------------------------
