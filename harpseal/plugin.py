"""
    harpseal.plugin
    ~~~~~~~~~~~~~~~

    Plugin class definition

"""
import asyncio
import inspect
from collections import defaultdict
from datetime import datetime
from importlib import import_module

from harpseal.utils.commands import execute
from harpseal.classes import PeriodicTask, StrictDict
from harpseal.models import make_model

class Plugin(object):
    """
    Base plugin model
    """
    name = ''
    description = ''
    priority = 0
    every = 1

    _app = None

    def __init__(self):
        self.models = {}
        self.fields = defaultdict(lambda: [])
        self.field_types = defaultdict(lambda: 'line')  # line, stack, full-stack, bar
        if hasattr(self, 'init'):
            self.init()
        for k, v in self.fields.items():
            self.fields[k] = tuple(v)
        self.init_model()
        self.last_executed_at = None
        self.last_executed_result = None

    def init_model(self):
        for name, fields in self.fields.items():
            modelname = '{}_{}'.format(self.name.title(), name)
            self.models[name] = make_model(modelname, fields)

    def data_form(self):
        form = {}
        for name, fields in self.fields.items():
            form[name] = StrictDict(fields)
        return form

    @asyncio.coroutine
    def execute(self):
        """
        Execute plugin
        """
        if not asyncio.iscoroutinefunction(self.provider):
            raise TypeError("You must wrap the function with '@asyncio.coroutine' decorator.")
        self.last_executed_at = datetime.now()
        try:
            data = yield from self.provider()
        except:
            data = None
            self.last_executed_result = False
        else:
            self.last_executed_result = True

        if data is None:
            print("WARNING: The data is not passed from the .provider() function.")
        return (self, data, )

    @asyncio.coroutine
    def call(self, command):
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
