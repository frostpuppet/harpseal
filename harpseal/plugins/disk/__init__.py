"""
harpseal.plugins.disk
~~~~~~~~~~~~~~~~~~~~

"""
import asyncio

import psutil

from harpseal.plugin import Plugin

class DiskPlugin(Plugin):
    name = 'disk'
    description = 'disk watch plugin'
    priority = 0
    every = 1

    def init(self):
        self.partitions = partitions = psutil.disk_partitions()
        for p in partitions:
            name = '{}_usage'.format(p.device.split('/')[-1])
            self.field_types[name] = 'stack'
            self.fields[name] = [('used', int, ), ('free', int, )]

        ios = psutil.disk_io_counters(perdisk=True)
        for device in ios.keys():
            name = '{}_io'.format(device)
            self.field_types[device] = 'line'
            for i in ['read_count', 'write_count', 'read_bytes', 'write_bytes',
                      'read_time', 'write_time']:
                self.fields[name].append((i, int, ))

    @asyncio.coroutine
    def provider(self):
        data = self.data_form()

        for p in self.partitions:
            name = '{}_usage'.format(p.device.split('/')[-1])
            usage = psutil.disk_usage(p.mountpoint)
            data[name].set('used', usage.used)
            data[name].set('free', usage.free)

        ios = psutil.disk_io_counters(perdisk=True)
        for device, values in ios.items():
            name = '{}_io'.format(device)
            for i in ['read_count', 'write_count', 'read_bytes', 'write_bytes',
                      'read_time', 'write_time']:
                data[name].set(i, getattr(values, i))

        return data
