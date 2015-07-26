"""
    Harpseal App
    ~~~~~~~~~~~~
    
    Harpseal app, includes web server and harpseal daemon.
"""
import asyncio
import aiohttp

from mongoengine import connect as mongo_connect

from harpseal.conf import Config
from harpseal.plugin import Plugin, PluginMixin
from harpseal.web import WebServer

__all__ = ['Harpseal']

class Harpseal(PluginMixin):
    """Harpseal daemon."""

    def __init__(self, conf='config.json'):
        """Initialize harpseal daemon.

        :param config: configuration file path
        """
        #: (:class:`asyncio.BaseEventLoop`) Base event-loop
        self.loop = None
        #: (:class:`harpseal.conf.Config`) Harpseal configuration
        self.config = Config(path=conf)
        #: (:class:`asyncio.Queue') Queue that saves plugin result to store data to mongodb
        self.queue = asyncio.Queue()
        #: (:class:`harpseal.web.WebServer`) Harpseal API server
        self.web = WebServer(self)
        #: (:class:`tuple`) Plugins
        self.plugins = tuple()
        #: (:class:`tuple`) Tasks (by plugins)
        self.tasks = tuple()

        Plugin._app = self

        conn_attrs = self.config['mongo']
        for k, v in conn_attrs.items():
            if k.startswith('_'):
                del conn_attrs[k]
        mongo_connect(**conn_attrs)

    @asyncio.coroutine
    def start(self, loop):
        """Start a web server and periodic task after register and execute plugins.

        :param loop: Base event-loop
        """
        self.loop = loop
        self.register_plugins()
        self.run_plugins()
        self.web_task = asyncio.Task(self.web.execute())
        done, *pending = yield from asyncio.wait([self.web_task, ])
        future, = done
        assert pending
        yield from self.periodic_task()

    @asyncio.coroutine
    def periodic_task(self):
        """Store a new mongo instance with given plugin data to mongodb when got a new result."""
        while 1:
            plugin, result = yield from self.queue.get()
            for name in result.keys():
                attrs = {}
                for key in result[name].keys():
                    attrs[key] = result[name].get(key)
                model = plugin.models[name]()
                model.add(**attrs)
                model.save()
