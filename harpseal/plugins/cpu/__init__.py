"""
harpseal.plugins.cpu
~~~~~~~~~~~~~~~~~~~~

"""
import asyncio

import psutil

from harpseal.plugin import Plugin

class CPUPlugin(Plugin):
    name = 'cpu'
    description = 'cpu watch plugin'
    priority = 0
    every = 1

    def init(self):
        self.field_types['cpu'] = 'line'
        self.field_types['cpu_times'] = 'full-stack'
        self.field_types['pids'] = 'line'

        cpus = psutil.cpu_count()
        for i in range(cpus):
            self.fields['cpu'].append(('cpu{}'.format(i), float, ))

        self.fields['cpu_times'] = ['user', 'nice', 'system', 'idle', 'iowait',
                                    'irq', 'softirq', 'steal', 'guest', 'guest_nice']
        self.fields['pids'] = ['count']

    @asyncio.coroutine
    def provider(self):
        pass
