"""
    harpseal.web.handler
    ~~~~~~~~~~~~~~~~~~~~

"""
import asyncio

from harpseal.utils import datetime as dtutils
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

    def get_plugin_list(self, withdetails=False):
        data = {
            name: {
                'description': item.description,
                'every': item.every,
                'lastExecutedAt': dtutils.unixtime(item.last_executed_at),
                'lastExecutedResult': item.last_executed_result,
            } for name, item in self.plugins.items()
        } if withdetails else self.plugins.keys()

        return data

    @asyncio.coroutine
    def plugin_list_handler(self, req):
        return Response(self.get_plugin_list(withdetails=True))

    @asyncio.coroutine
    @plugin_required
    def plugin_handler(self, req):
        name = req.match_info.get('name')
        return Response({'name': name})
