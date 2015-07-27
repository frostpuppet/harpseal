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
        try:
            body = json.loads(body.decode('utf-8'))
        except:
            pass
        return (req, body, )

    @async_test
    def test(self, loop):
        task = yield from self.initapp(loop)
        yield from asyncio.sleep(3)
        
        req, body = yield from self.get('/')
        assert req.status == 404

        req, body = yield from self.get('/plugins/list')
        assert req.status == 200
        assert 'cpu' in body
        assert body['cpu']['lastExecutedResult'] == True

        req, body = yield from self.get('/plugins/cpu')
        assert req.status == 200
        assert 'data' in body
