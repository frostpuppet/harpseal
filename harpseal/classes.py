"""
    harpseal.classes
    ~~~~~~~~~~~~~~~~

    Classes, include Mixin, Task and others
"""
import asyncio

class PeriodicTask(object):
    """
    Make a periodic task
    """

    def __init__(self, interval, func, app):
        self._interval = interval
        self._func = func
        self._app = app

    def _run(self):
        self.run()
        self._handler = self._app.loop.call_later(self._interval, self._run)

    def run(self):
        result = None
        if self._func.__name__ == 'coroutine':
            result = yield from self._func()
        else:
            result = self._func()
        if result is not None:
            yield from self._app.queue.put(result)

    def start(self):
        self._handler = self._app.loop.call_later(self._interval, self._run)

    def stop(self):
        self._handler.cancel()
