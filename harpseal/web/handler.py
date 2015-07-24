"""
    harpseal.web.handler
    ~~~~~~~~~~~~~~~~~~~~

"""
import asyncio

from harpseal.web import Response

__all__ = ['Handler']

def plugin_required(func):
    def decorator(self, req):
        name = req.match_info.get('name')
        if name not in self.plugins.keys():
            return Response({'ok': False, 'reason': 'Plugin does not exist.'})
        return func(self, req)
    return decorator


class Handler(object):
    def __init__(self, plugins):
        self.plugins = {plugin.name: plugin for plugin in plugins}

    @asyncio.coroutine
    @plugin_required
    def plugin_handler(self, req):
        name = req.match_info.get('name')
        return Response({'name': name})
