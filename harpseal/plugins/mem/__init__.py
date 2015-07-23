"""
harpseal.plugins.mem
~~~~~~~~~~~~~~~~~~~~

"""
import asyncio
import inspect
from collections import defaultdict

import psutil

from harpseal.plugin import Plugin

class MemPlugin(Plugin):
    name = 'mem'
    description = 'memory watch plugin'
    priority = 0
    every = 1

    def init(self):
        self.memtypes = defaultdict(lambda: [])
        for memtype, method in [('virtual', psutil.virtual_memory, ), ('swap', psutil.swap_memory, )]:
            run = method()
            keys = [m for m in dir(run) if not m.startswith('_') and isinstance(getattr(run, m), int)]
            self.memtypes[memtype] = (keys, method, )
            self.field_types[memtype] = 'stack'
            for key in keys:
                self.fields[memtype].append((key, int, ))

    @asyncio.coroutine
    def provider(self):
        data = self.data_form()
        for memtype in ['virtual', 'swap']:
                keys, method = self.memtypes[memtype]
                item = method()
                for key in keys:
                    data[memtype].set(key, getattr(item, key))
        return data
