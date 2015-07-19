"""
harpseal.app
~~~~~~~~~~~~

:copyright: (c) 2015 by SuHun Han (ssut).
:license: GPL v2, see LICENSE for more details.
"""
import asyncio

class Harpseal(object):
    def __init__(self):
        self.loop = None

    @asyncio.coroutine
    def start(self, loop):
        self.loop = loop
