"""
    harpseal.web.router
    ~~~~~~~~~~~~~~~~~~~

"""
import asyncio
import json

from aiohttp import web

from harpseal.web.handler import Handler

__all__ = ['Router']

class Router(object):
    def __init__(self, app, plugins):
        self.parent = app  # WebServer
        self.handler = Handler(plugins=plugins)
        app.router.add_route('GET', r'/plugins/{name}', self.handler.plugin_handler)
