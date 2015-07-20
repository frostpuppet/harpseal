"""
harpseal.app
~~~~~~~~~~~~

:copyright: (c) 2015 by SuHun Han (ssut).
:license: GPL v2, see LICENSE for more details.
"""
import asyncio
import aiohttp

from harpseal.web import WebServer

class Harpseal(object):
    def __init__(self):
        self.loop = None
        self.web = WebServer(self)

    @asyncio.coroutine
    def start(self, loop):
        self.loop = loop
        self.web_task = asyncio.Task(self.web.execute())
        self.beat_task = asyncio.Task(self.beats())
        yield from asyncio.wait([self.web_task, self.beat_task, ])
        yield from self.periodic_task()

    @asyncio.coroutine
    def periodic_task(self):
        while 1:
            # TODO: get a task from the queue and execute then grab and store its result
            yield from asyncio.sleep(1)

    @asyncio.coroutine
    def beats(self):
        pass
