"""
    harpseal.web.handler
    ~~~~~~~~~~~~~~~~~~~~

"""
import asyncio
from datetime import datetime

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

    def get_plugin_logs(self, name, gte, lte=None):
        if name not in self.plugins.keys():
            raise KeyError("Plugin does not exist.")
        if lte is None:
            lte = datetime.now()

        data = {}
        plugin = self.plugins[name]
        for k, v in plugin.fields.items():
            fielddata = {
                'type': plugin.field_types[k],
                'legends': ['created'] + [n for n, _ in v],
                'data': [],
            }
            records = plugin.models[k].objects(created_at__gte=gte,
                                               created_at__lte=lte)
            for record in records:
                items = [dtutils.unixtime(record.created_at)]
                for n, _ in v:
                    items.append(getattr(record.items, n))
                fielddata['data'].append(items)
            data[k] = fielddata

        return data

    @asyncio.coroutine
    def plugin_list_handler(self, req):
        return Response(self.get_plugin_list(withdetails=True))

    @asyncio.coroutine
    @plugin_required
    def plugin_handler(self, req):
        name = req.match_info.get('name')
        plugin = self.get_plugin_list(withdetails=True)[name]
        data = self.get_plugin_logs(name, gte=dtutils.ago(days=7))
        data = {
            'name': name,
            'data': data,
        }
        data.update(plugin)

        return Response(data)
