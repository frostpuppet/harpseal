"""
    harpseal.web.handler
    ~~~~~~~~~~~~~~~~~~~~

"""
import asyncio

from harpseal.web import Response

class Handler(object):
    def __init__(self, plugins):
        self.plugins = {plugin.name: plugin for plugin in plugins}

    @asyncio.coroutine
    def plugin_handler(self, req):
        name = req.match_info.get('name')
        return Response({'name': name})
