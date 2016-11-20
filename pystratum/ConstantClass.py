"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import importlib
import inspect
import re


class ConstantClass:
    """
    Helper class for loading and modifying the class that acts like a namespace for constants.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, class_name, io):
        """
        Object constructor.

        :param str class_name: The name of class that acts like a namespace for constants.
        :param pystratum.style.PyStratumStyle.PyStratumStyle io: The output decorator.
        """
        self.__class_name = class_name
        """
        The name of class that acts like a namespace for constants.

        :type: str
        """

        self.__module = None
        """
        The module of which the class that acts like a namespace for constants belongs.

        :type: module
        """

        self.__annotation = '# PyStratum'
        """
        The comment after which the auto generated constants must be inserted.

        :type: str
        """

        self._io = io
        """
        The output decorator.

        :type: pystratum.style.PyStratumStyle.PyStratumStyle
        """

        self.__load()

    # ------------------------------------------------------------------------------------------------------------------
    def __load(self):
        """
        Loads dynamically the class that acts like a namespace for constants.
        """
        parts = self.__class_name.split('.')
        module_name = ".".join(parts[:-1])
        module = __import__(module_name)
        modules = []
        for comp in parts[1:]:
            module = getattr(module, comp)
            modules.append(module)

        self.__module = modules[-2]

    # ------------------------------------------------------------------------------------------------------------------
    def file_name(self):
        """
        Returns the filename of the module with the class that acts like a namespace for constants.

        :rtype: str
        """
        return inspect.getfile(self.__module)

    # ------------------------------------------------------------------------------------------------------------------
    def source(self):
        """
        Returns the source of the module with the class that acts like a namespace for constants.

        :rtype: str
        """
        return inspect.getsource(self.__module)

    # ------------------------------------------------------------------------------------------------------------------
    def reload(self):
        """
        Reloads the module with the class that acts like a namespace for constants.
        """
        importlib.reload(self.__module)

    # ------------------------------------------------------------------------------------------------------------------
    def constants(self):
        """
        Gets the constants from the class that acts like a namespace for constants.

        :rtype: dict<str,*>
        """
        ret = {}

        name = self.__class_name.split('.')[-1]
        constant_class = getattr(self.__module, name)
        for name, value in constant_class.__dict__.items():
            if re.match(r'^[A-Z][A-Z0-9_]*$', name):
                ret[name] = value

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def __extract_info(self, lines):
        """
        Extracts the following info from the source of the module with the class that acts like a namespace for
        constants:
        * Start line with constants
        * Last line with constants
        * Indent for constants

        :param list[str] lines: The source of the module with the class that acts like a namespace for constants.

        :rtype: dict<str,int|str>
        """
        ret = {'start_line': 0,
               'last_line':  0,
               'indent':     ''}

        mode = 1
        count = 0
        for line in lines:
            if mode == 1:
                if line.strip() == self.__annotation:
                    ret['start_line'] = count + 1
                    ret['last_line'] = count + 1
                    parts = re.match(r'^(\s+)', line)
                    ret['indent'] = parts.group(1)
                    mode = 2

            elif mode == 2:
                if line.strip() == '' or line.strip()[0:1] == '#':
                    mode = 3
                else:
                    ret['last_line'] = count + 1

            else:
                break

            count += 1

        if mode != 3:
            raise RuntimeError("Unable to find '{}' in file {}".format(self.__annotation, self.source()))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def source_with_constants(self, constants):
        """
        Returns the source of the module with the class that acts like a namespace for constants with new constants.

        :param dict[str,int] constants: The new constants.

        :rtype: str
        """
        old_lines = self.source().split("\n")
        info = self.__extract_info(old_lines)

        new_lines = old_lines[0:info['start_line']]

        for constant, value in sorted(constants.items()):
            new_lines.append("{0}{1} = {2}".format(info['indent'], str(constant), str(value)))

        new_lines.extend(old_lines[info['last_line']:])

        return "\n".join(new_lines)

# ----------------------------------------------------------------------------------------------------------------------
