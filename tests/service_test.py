import asyncio
import aiohttp
import json

import unittest
from pytest import fixture, mark, raises

from harpseal.app import Harpseal

def async_test(f):
    def decorator(*args, **kwargs):
        loop = asyncio.get_event_loop()
        coro = asyncio.coroutine(f)
        kwargs['loop'] = loop
        future = coro(*args, **kwargs)
        loop.run_until_complete(future)
    return decorator

class TestHarpseal(unittest.TestCase):
    @asyncio.coroutine
    def initapp(self, loop):
        app = Harpseal(conf='config.sample.json')
        app_task = asyncio.Task(app.start(loop))
        for task in app.tasks:
            task._interval = 2
        return app

    @asyncio.coroutine
    def get(self, path):
        data = None
        req = yield from aiohttp.request('get', 'http://127.0.0.1:24680{}'.format(path))
        body = yield from req.read_and_close()
        body = body.decode('utf-8')
        try:
            body = json.loads(body)
        except:
            pass
        return (req, body, )

    @async_test
    def test(self, loop):
        task = yield from self.initapp(loop)
        yield from asyncio.sleep(3)
        
        req, body = yield from self.get('/')
        assert req.status == 404

        # Test for plugin list
        req, body = yield from self.get('/plugins/list')
        assert req.status == 200
        assert 'cpu' in body
        assert body['cpu']['lastExecutedResult'] == True

        # Test for expected plugin
        req, body = yield from self.get('/plugins/cpu')
        assert req.status == 200
        assert 'data' in body

        # Test for unexpected plugin
        req, body = yield from self.get('/plugins/asdffoobar')
        assert req.status == 200
        assert 'ok' in body
        assert not body['ok']

        # Test for comptarget method
        req, body = yield from self.get('/plugins/cpu?gte=weird')
        assert req.status == 200
        assert 'ok' in body
        assert not body['ok']

        # Test for plugins_handler method
        req, body = yield from self.get('/plugins/all')
        assert 'ok' in body
        assert body['ok']

        # Test for comptarget method over plugins_handler method
        req, body = yield from self.get('/plugins/all?gte=weird')
        assert req.status == 200
        assert 'ok' in body
        assert not body['ok']

        # Test for jsonp callback
        req, body = yield from self.get('/plugins/list?callback=$.test')
        assert req.status == 200
        assert '$.test({' in body
