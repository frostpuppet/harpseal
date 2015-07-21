"""
    harpseal.plugin
    ~~~~~~~~~~~~~~~

    Plugin class definition

"""
import asyncio
import inspect
from importlib import import_module

from harpseal.utils.commands import execute
from harpseal.classes import PeriodicTask

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
        if not asyncio.iscoroutinefunction(self.provider):
            raise TypeError("You must wrap the function with '@asyncio.coroutine' decorator.")
        data = yield from self.provider()
        if data is None:
            raise AssertionError("The data is not passed from the .provider() function.")
        return data

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

class _PluginMixin(object):
    @staticmethod
    def plugin_mixin_assert(func):
        def decorator(self):
            if self.__class__.__name__ != 'Harpseal':
                raise AssertionError("This mixin class must be inherited from 'Harpseal' class.")
            if not hasattr(self, 'plugins') or not isinstance(self.plugins, tuple):
                raise TypeError("The .plugins attribute must be a tuple.")
            func(self)
        return decorator

class PluginMixin(_PluginMixin):
    """
    Mixin class for Plugin management
    """

    @_PluginMixin.plugin_mixin_assert
    def register_plugins(self):
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
                self.plugins += (instance, )

    @_PluginMixin.plugin_mixin_assert
    def run_plugins(self):
        for plugin in self.plugins:
            task = PeriodicTask(plugin=plugin, app=self)
            task.start()
            self.tasks += (task, )


