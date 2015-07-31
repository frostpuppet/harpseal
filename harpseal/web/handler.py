"""
    Web Handler
    ~~~~~~~~~~~

"""
import asyncio
import aiohttp
import json
from aiohttp import web
from datetime import datetime

from harpseal.utils import datetime as dtutils
from harpseal.web.classes import MockRequest
from harpseal.web import Response

__all__ = ['Handler']

def plugin_required(func):
    """Check if requested plugin is exists."""
    def decorator(self, req):
        name = req.match_info.get('name')
        if name not in self.plugins.keys():
            return Response({'ok': False, 'reason': 'Plugin does not exist.'})
        return func(self, req)
    return decorator


class Handler(object):
    """Handler object."""

    def __init__(self, plugins):
        self.plugins = {plugin.name: plugin for plugin in plugins}

    def raise_error(self, reason=''):
        """Create an dict that represents error during the handling of the request."""
        error = {
            'ok': False,
            'reason': reason,
        }
        return Response(error)

    def parse_comptarget(self, req):
        """Prase GET fragments that would includes optional arguments such as `gte` and `lte`."""
        gte, lte = req.GET.get('gte', None), req.GET.get('lte', None)
        try:
            gte = dtutils.parse(gte) if gte else dtutils.ago(days=7)
            lte = dtutils.parse(lte) if lte else datetime.now()
        except:
            gte, lte = None, None
        return (gte, lte, )

    def get_plugin_list(self, withdetails=False):
        """Get plugin list.

        :param bool withdetails: True if you want to get plugin list with details.
        """
        data = {
            name: {
                'description': item.description,
                'every': item.every,
                'lastExecutedAt': dtutils.unixtime(item.last_executed_at) if item.last_executed_at else None,
                'lastExecutedResult': item.last_executed_result,
            } for name, item in self.plugins.items()
        } if withdetails else self.plugins.keys()

        return data

    def get_plugin_logs(self, name, gte, lte=None):
        """Get plugin logs.

        :param str name: Plugin name
        :param gte: Greater than or equal to (created time)
        :param lte: Less than or equal to (created time)
        """
        if name not in self.plugins.keys():
            raise KeyError("Plugin does not exist.")

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
    def websocket_handler(self, req):
        """Handling websocket connections."""
        ws = web.WebSocketResponse()
        ws.start(req)

        routes = {}
        for name in dir(self):
            if name.endswith('_handler'):
                routename = name[:-8]
                routes[routename] = getattr(self, name)

        while True:
            msg = yield from ws.receive()
            if msg.tp == aiohttp.MsgType.text:
                try:
                    data = json.loads(msg.data)
                except ValueError:
                    error = json.dumps({'error': True, 'reason': 'You must pass a JSON string.'})
                    ws.send_str(error)
                else:
                    if 'close' in data:
                        yield from ws.close()
                    else:
                        handler = data.get('request', '')
                        match_info = {k: v for k, v in data.items() if k not in ('request', 'params', )}
                        params = {k: str(v) for k, v in data.get('params', {}).items()}
                        mock = MockRequest(get=params, match_info=match_info)
                        if not handler or handler not in routes:
                            error = json.dumps({'error': True, 'reason': 'You must pass a handler name.'})
                            ws.send_str(error)
                        else:
                            resp = yield from routes[handler](mock)
                            body = resp._body.decode('utf-8')
                            ws.send_str(body)
            elif msg.tp == aiohttp.MsgType.close:
                print('websocket connection closed')
            elif msg.tp == aiohttp.MsgType.error:
                print('ws connection closed with exception %s',
                      ws.exception())

        return ws

    @asyncio.coroutine
    def plugin_list_handler(self, req):
        """Return plugin list."""
        return Response(self.get_plugin_list(withdetails=True))

    @asyncio.coroutine
    @plugin_required
    def plugin_handler(self, req):
        """Return specified plugin logs."""
        gte, lte = self.parse_comptarget(req)
        if gte is None or lte is None:
            return self.raise_error('The given datetime cannot be parsed.')
        name = req.match_info.get('name')

        plugin = self.get_plugin_list(withdetails=True)[name]
        data = self.get_plugin_logs(name, gte=gte, lte=lte)
        data = {
            'name': name,
            'data': data,
        }
        data.update(plugin)

        return Response(data)

    @asyncio.coroutine
    def plugins_handler(self, req):
        """Return all plugin logs."""
        gte, lte = self.parse_comptarget(req)
        if gte is None or lte is None:
            return self.raise_error('The given datetime cannot be parsed.')

        plugins = self.get_plugin_list(withdetails=True)
        data = {'data': {}}
        for name, details in plugins.items():
            data['data'][name] = details
            data['data'][name]['data'] = self.get_plugin_logs(name, gte=gte, lte=lte)

        return Response(data)
