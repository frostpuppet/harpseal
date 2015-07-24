"""
    harpseal.web.router
    ~~~~~~~~~~~~~~~~~~~

"""
import asyncio

from aiohttp import web

from harpseal.web.handler import Handler

__all__ = ['Router']

class Router(object):
    def __init__(self, app, plugins):
        self.parent = app  # WebServer
        self.handler = Handler(plugins=plugins)
        self.add_routes()

    def add_routes(self):
        self.parent.router.add_route(
            'GET', r'/plugins/list', self.handler.plugin_list_handler)
        self.parent.router.add_route(
            'GET', r'/plugins/{name}', self.handler.plugin_handler)

