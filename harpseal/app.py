"""
    harpseal.app
    ~~~~~~~~~~~~
    
    Harpseal app, includes web server and harpseal daemon
"""
import asyncio
import aiohttp

from harpseal.conf import Config
from harpseal.plugin import Plugin, PluginMixin
from harpseal.web import WebServer

class Harpseal(PluginMixin):
    def __init__(self, conf='config.json'):
        self.loop = None
        self.web = WebServer(self)
        self.queue = asyncio.Queue()
        self.config = Config(path=conf)
        self.plugins = tuple()
        self.tasks = tuple()
        Plugin._app = self

    @asyncio.coroutine
    def start(self, loop):
        self.loop = loop
        self.register_plugins()
        self.run_plugins()
        self.web_task = asyncio.Task(self.web.execute())
        yield from asyncio.wait([self.web_task, ])
        yield from self.periodic_task()

    @asyncio.coroutine
    def periodic_task(self):
        while 1:
            result = yield from self.queue.get()
            print(result)
