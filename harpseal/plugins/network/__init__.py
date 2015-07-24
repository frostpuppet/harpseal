"""
    harpseal.plugins.network
    ~~~~~~~~~~~~~~~~~~~~~~~~

"""
import asyncio
import inspect
from collections import defaultdict

import psutil

from harpseal.plugin import Plugin

class NetworkPlugin(Plugin):
    name = 'network'
    description = 'network watch plugin'
    priority = 0
    every = 1

    def init(self):
        self.transferred = {
            'DL': {},
            'UP': {},
        }
        counters = psutil.net_io_counters(pernic=True)
        self.interfaces = [i for i, _ in counters.items() if i != 'lo']  # exclude local loopback
        for interface in self.interfaces:
            trfname = '{}_traffic'.format(interface)
            self.transferred['DL'][interface] = None
            self.transferred['UP'][interface] = None
            self.field_types[interface] = 'line'
            self.field_types[trfname] = 'line'
            first = counters[list(counters.keys())[0]]
            keys = [k for k in dir(first) if not k.startswith('_') and isinstance(getattr(first, k), int)]
            for key in keys:
                self.fields[interface].append((key, int, ))
            self.fields[trfname] = [('download', float, ), ('upload', float, ), ]

    @asyncio.coroutine
    def provider(self):
        data = self.data_form()
        isnew = False
        counters = psutil.net_io_counters(pernic=True)
        for interface in self.interfaces:
            trfname = '{}_traffic'.format(interface)
            if self.transferred['DL'][interface] is None or self.transferred['UP'][interface] is None:
                isnew = True
            if not isnew:
                dldiff = counters[interface].bytes_recv - self.transferred['DL'][interface]
                updiff = counters[interface].bytes_sent - self.transferred['UP'][interface]
                # download/upload rate per second
                dlps = float(dldiff) / (NetworkPlugin.every * 60)
                upps = float(updiff) / (NetworkPlugin.every * 60)
                data[trfname].set('download', dlps)
                data[trfname].set('upload', upps)
                for name, _ in self.fields[interface]:
                    data[interface].set(name, getattr(counters[interface], name))

            self.transferred['DL'][interface] = counters[interface].bytes_recv
            self.transferred['UP'][interface] = counters[interface].bytes_sent

        data = None if isnew else data
        return data
