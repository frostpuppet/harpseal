"""
    harpseal.web.classes
    ~~~~~~~~~~~~~~~~~~~~

"""
import asyncio

from aiohttp import web

__all__ = ['Response']

class Response(web.StreamResponse):
    def __init__(self, body=None, status=200, reason=None, headers=None):
        super().__init__(status=status, reason=reason, headers=headers)

        if body is None:
            raise ValueError("the argument 'body' is positional argument.")
        self.headers['Content-Type'] = self.content_type = 'application/json'
        self.body = body

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, data):
        if data is not None and not isinstance(data, dict):
            raise TypeError('data argument must be dict.')

        if self.charset is None:
            self.charset = 'utf-8'

        body = json.dumps(data).encode(self.charset)
        self._body = body
        self.content_length = len(body) if body is not None else 0

    @asyncio.coroutine
    def write_eof(self):
        body = self._body
        if body is not None:
            self.write(body)
