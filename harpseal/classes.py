"""
    harpseal.classes
    ~~~~~~~~~~~~~~~~

    Classes, include Mixin, Task and others
"""
import asyncio

__all__ = ['PeriodicTask', 'StrictDict']

class PeriodicTask(object):
    """
    Make a periodic task
    """

    def __init__(self, plugin, app):
        self.plugin = plugin
        self._interval = plugin.properties['every']
        self._func = plugin.execute
        self._app = app
        self._task = None

    @asyncio.coroutine
    def _run(self):
        while 1:
            yield from asyncio.sleep(self._interval)
            yield from self.run()

    @asyncio.coroutine
    def run(self):
        result = yield from self._func()
        if result is not None:
            yield from self._app.queue.put(result)

    def start(self):
        self._task = asyncio.Task(self._run())


class StrictDict(object):
    def __init__(self, fields):
        self._fields = fields
        self._keys = [k for k, _ in self._fields]
        self._types = {k: t for k, t in self._fields}
        self._values = {k: None for k, _ in self._fields}

    def get(self, name):
        if name not in self._keys:
            raise KeyError("The key '{}' does not exist in the dict.".format(name))
        return self._values.get(name)

    def set(self, name, value):
        if name not in self._keys:
            raise KeyError("The key '{}' does not exist in the dict.".format(name))
        if not isinstance(value, self._types[name]):
            raise TypeError("TypeError")
        self._values[name] = value

    def keys(self):
        return self._keys
