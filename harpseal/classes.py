"""
    Harpseal Classes
    ~~~~~~~~~~~~~~~~

    Classes, include Mixin, Task and others.
"""
import asyncio

__all__ = ['PeriodicTask', 'StrictDict']

class PeriodicTask(object):
    """A class for creating periodic task."""

    def __init__(self, plugin, app):
        #: (:class:`harpseal.plugin.Plugin`) Target plugin to run periodically
        self.plugin = plugin
        self._interval = plugin.properties['every'] * 60
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
        """Execute plugin and then put the result into app's queue."""
        plugin, result = yield from self._func()
        if result is not None:
            yield from self._app.queue.put((plugin, result, ))

    def start(self):
        """Start a periodic task."""
        self._task = asyncio.Task(self._run())


class StrictDict(object):
    """A dictionary-like semi-dynamic dict class.
    Values are stored in strictly with the field types given.
    """

    def __init__(self, fields):
        self._fields = fields
        self._keys = [k for k, _ in self._fields]
        self._types = {k: t for k, t in self._fields}
        self._values = {k: None for k, _ in self._fields}

    def get(self, name):
        """Get a value of `name` key."""
        if name not in self._keys:
            raise KeyError("The key '{}' does not exist in the dict.".format(name))
        return self._values.get(name)

    def set(self, name, value):
        """Set a value of `name` key; to be stored in strictly (type-sensitive)."""
        if name not in self._keys:
            raise KeyError("The key '{}' does not exist in the dict.".format(name))
        if not isinstance(value, self._types[name]):
            raise TypeError("TypeError")
        self._values[name] = value

    def keys(self):
        """Return the keys of dict. The result is not a kind of `view`."""
        return self._keys
