"""
    Web Classes
    ~~~~~~~~~~~

"""
import asyncio
import json

from aiohttp import web

__all__ = ['Response']

class Response(web.StreamResponse):
    """Response object."""
    def __init__(self, body=None, status=200, reason=None, headers=None):
        super().__init__(status=status, reason=reason, headers=headers)

        if body is None:
            raise ValueError("the argument 'body' is positional argument.")
        elif 'ok' not in body:
            body['ok'] = True
        self.headers['Content-Type'] = self.content_type = 'application/json'
        #: (:class:`byte`) Response content (`utf-8` data)
        self.body = body

    @property
    def body(self):
        """`body` getter"""
        return self._body

    @body.setter
    def body(self, data):
        """`body` setter; this method checks if data is available, and convert to json format."""
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
        yield from super().write_eof()
