"""
    harpseal.plugin
    ~~~~~~~~~~~~~~~

    Plugin class definition

"""
import asyncio
import inspect
from importlib import import_module

from harpseal.utils.commands import execute

class Plugin(object):
    """
    Base plugin model
    """
    name = ''
    description = ''
    priority = 0
    every = 1

    _app = None

    @asyncio.coroutine
    def execute(self):
        """
        Execute plugin
        """
        if self.provider.__name__ != 'coroutine':
            raise TypeError("You must wrap the function with '@asyncio.coroutine' decorator.")
        data = yield from self.provider()
        if data is None:
            raise AssertionError("The data is not passed from the .provider() function.")

    @asyncio.coroutine
    def _call(self, command):
        """
        Execute a command on the event-loop and then return the result when finished.
        """
        if Plugin._app is None:
            raise AssertionError("The property ._app is not assigned.")
        result = yield from execute(Plugin._app, command)
        return result

    @asyncio.coroutine
    def provider(self):
        """
        Plugin provider that returns a plugin's result.
        """
        raise NotImplementedError(".provider() must be overridden.")

    @property
    def properties(self):
        """
        Return the instance properties as a dict.
        """
        if self.name == '' or self.description == '':
            raise ValueError("You must set the variables for both .name and .description.")
        properties = {
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
            'every': self.every,
        }
        return properties

class PluginMixin(object):
    """
    Mixin class for Plugin management
    """
    def _plugin_mixin_assert(self):
        if self.__class__.__name__ != 'Harpseal':
            raise AssertionError("This mixin class must be inherited from 'Harpseal' class.")
        if not hasattr(self, 'plugins') or not isinstance(self.plugins, tuple):
            raise TypeError("The .plugins attribute must be a tuple.")

    def register_plugins(self):
        self._plugin_mixin_assert()
        for name in self.config['plugins']:
            modname = 'harpseal.plugins.{}'.format(name)
            plugin = None
            try:
                plugin = import_module(modname)
            except ImportError:
                raise RuntimeWarning("Cannot load {} plugin due to import error.".format(modname))
            else:
                _, cls = inspect.getmembers(plugin,
                    lambda member: inspect.isclass(member) and \
                           member.__module__ == modname)[0]
                instance = cls()
                self.plugins += (plugin, )

