"""

Lite plugins for simple Python 3 projects
Mikhail Zakharov <zmey20000@yahoo.com>, 2020

"""

import os
import sys

import re


class LTPlugins:
    """
    Lite plugins management

    :param path: specifies plugin location directory within the script directory, if empty, current directory is used
    :param prefix: all modules with the prefix are considered plugins
    :param plugin: a plugin Name to work with

    :property plugin_path: Contains an absolute path to the plugins directory
    :property name[plugin]: A dictionary with names of loaded plugins
    """

    def __init__(self, path='plugins', prefix='ltp_', plugin=''):
        if path:
            self.plugin_path = os.path.join(sys.path[0], path)
            if self.plugin_path not in sys.path:
                sys.path.append(self.plugin_path)

        self.prefix = prefix
        self.name = dict()
        if plugin:
            self.load(plugin)

    def __str__(self):
        return str(self.name.keys())

    def __repr__(self):
        return str(self.name)

    def _loaded(self, plugin):
        """
        Check whether a plugin is loaded or not

        :param plugin: a plugin Name to check
        :returns: True if the plugin is loaded or False if not
        """
        return True if plugin in self.name else False

    def list(self, state='a', status=False):
        """
        List plugins by their status

        :param state: Takes one of: (a)ll, (l)oaded, (u)nloaded
        :param status: Show plugin status as tuple or not when listing output
        :returns: a list of plugins with selected status for loaded/unloaded and a list of tuples if 'all' is selected
        """

        result = []
        for plugin in os.listdir(self.plugin_path):
            plugin_name = re.search(f'{self.prefix}(.*?).py', plugin)
            if plugin_name:
                name = plugin_name.group(1)
                if state.lower() == 'l' and self._loaded(name):
                    result.append(status and (name, self._loaded(name)) or name)
                elif state.lower() == 'u' and not self._loaded(name):
                    result.append(status and (name, self._loaded(name)) or name)
                else:
                    result.append(status and (name, self._loaded(name)) or name)

        return result

    def load(self, plugin):
        """
        Load a plugin

        :param plugin: Plugin Name to load
        :returns: A reference to loaded plugin. Adds the plugin name to a dictionary: name[plugin]
        """

        if not self._loaded(plugin):
            self.name[plugin] = __import__(f'{self.prefix}{plugin}')
            return self.name[plugin]

    def unload(self, plugin):
        """
        Unloads a plugin from memory

        :param plugin: a plugin Name to unload
        :return: Nothing or rises NameError if trying to unload an unloaded plugin
        """

        if self._loaded(plugin):
            # Try to delete all the references to the plugin
            del sys.modules[f'{self.prefix}{plugin}']
            del self.name[plugin]
        else:
            raise NameError(f'The plugin: [{plugin}] has not been loaded')

    def reload(self, plugin):
        """
        Reload a plugin

        :param plugin: a plugin name to reload
        :return: a reference to the reloaded plugin module
        """

        if self._loaded(plugin):
            self.unload(plugin)
        return self.load(plugin)

    def run(self, plugin, function, *args, **kwargs):
        """

        Run a function from a plugin

        :param plugin: A name of the plugin
        :param function: A function to execute
        :param args: Function arguments
        :param kwargs: Keyworded arguments of the function
        :return: whatever a plugin function returns
        """

        if not self._loaded(plugin):
            self.load(plugin)
        if self._loaded(plugin):
            f = getattr(self.name[plugin], function)
            return f(*args, **kwargs)


if __name__ == "__main__":
    import __about__
    print(__about__.about)
