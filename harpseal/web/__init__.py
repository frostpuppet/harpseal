"""
harpseal.web
~~~~~~~~~~~~

"""
import asyncio

from aiohttp import web
from IPy import IP

from harpseal.web.classes import Response
from harpseal.web.router import Router

__all__ = ['WebServer', 'Resposne']

class WebServer(object):
    def __init__(self, parent):
        self.parent = parent
        self.app = None
        self.handler = None
        self.server = None
        self.router = None
        self.whitelist = [IP(allow) for allow in parent.config['server']['allows']]

    def __del__(self):
        yield from self.handler.finish_connections(1.0)
        self.server.close()
        yield from self.server.wait_closed()
        yield from self.app.finish()

    @asyncio.coroutine
    def whitelist_middleware(self, app, handler):
        @asyncio.coroutine
        def middleware(req):
            peername = req.transport.get_extra_info('peername')
            if peername is not None:
                host, port = peername
                isinwhites = any([host in white for white in self.whitelist])
                if not isinwhites:
                    error = {
                        'ok': False,
                        'reason': 'Your ipaddress is not in the whitelist of allowed IPs.',
                    }
                    return Response(error)
            return (yield from handler(req))
        return middleware

    @asyncio.coroutine
    def execute(self):
        self.app = web.Application(middlewares=[self.whitelist_middleware])
        self.handler = self.app.make_handler()
        self.server = self.parent.loop.create_server(self.handler,
                                                     self.parent.config['server']['host'],
                                                     self.parent.config['server']['port'])
        yield from self.server
        self.router = Router(self.app, plugins=self.parent.plugins)
