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

        for i in psutil.cpu_times_percent()._fields:
            self.fields['cpu_times'].append((i, float, ))
        self.fields['pids'] = [('count', int, )]

    @asyncio.coroutine
    def provider(self):
        data = self.data_form()
        cpu_percent = [i / 100.0 for i in psutil.cpu_percent(interval=1, percpu=True)]
        for i, value in enumerate(cpu_percent):
            data['cpu'].set('cpu{}'.format(i), value)
        cpu_times = psutil.cpu_times_percent(interval=1)
        for key in cpu_times._fields:
            data['cpu_times'].set(key, getattr(cpu_times, key))
        data['pids'].set('count', len(psutil.pids()))
        return data
