"""
harpseal.web
~~~~~~~~~~~~

"""
import asyncio
from aiohttp import web

class WebServer(object):
    def __init__(self, parent):
        self.parent = parent
        self.app = None
        self.handler = None
        self.server = None

    def __del__(self):
        yield from self.handler.finish_connections(1.0)
        self.server.close()
        yield from self.server.wait_closed()
        yield from self.app.finish()

    @asyncio.coroutine
    def execute(self):
        self.app = web.Application()
        self.handler = self.app.make_handler()
        self.server = self.parent.loop.create_server(self.handler, '0.0.0.0', 24680)
        yield from self.server
