Harpseal
========
*Harpseal* is a python app that collects system resources, usage and others by plugins which are extendable. *Harpseal* gives you easy accessible API to draw a graph or to analysis data by JSON format.

* GitHub: https://github.com/ssut/harpseal
* Issue tracker: https://github.com/ssut/harpseal/issues
* Telegram: `@ssssut <https://telegram.me/ssssut>`_
* Free software: `Apache License <http://opensource.org/licenses/Apache-2.0>`_

Features
--------

* Plugin — *Harpseal* is built upon a plugin system which allows support for new plugin to be easily created and added. It's quite easy in fact as you can see in this documentation. even you don't know anything about Harpseal structures.

* HTTP API - JSON/JSONP (callback)

  * It is possible to create a cluster monitoring system with **super simple** HTTP API.

  * As I've written above, even you can get jsonp callback mechanism; the more easily, you can create it with **Javascript** only.

* Light-weighted: with event-driven. *Harpseal* requires a lower memory footprint than many of system resource monitoring tools.

* Free. *Harpseal* is totally free to use even for commercial purposes.

* Super easy to install: it's super easy to install and set up *Harpseal* server on your Debian-based linux distros because it's already ready.


Getting Started
---------------

Dependencies
~~~~~~~~~~~~

`Harpseal` requires the following dependencies:

* Python 3.3 and `asyncio <https://aiohttp.readthedocs.org/en/stable/glossary.html#term-asyncio>`_ or Python 3.4+
* ``aiohttp`` library
* ``psutil`` library for built-in plugins
* ``mongoengine`` library for data storage
* ``IPy`` library

Installation
~~~~~~~~~~~~

(TBA)

Configuration
~~~~~~~~~~~~~

(TBA with installation)

Built-in Plugins
~~~~~~~~~~~~~~~~

* `cpu` - CPU watch plugin; it watches for each CPU usage, PID count and CPU times.
* `mem` - Memory watch plugin; it watches for detailed memory usage data including swap memory.
* `disk` - Disk watch plugin; it watches for each disk IOs and spaces.
* `net` - Network watch plugin; it logs for network statistics.

HTTP API
--------

(TBA)

Creating Plugins
----------------

(TBA)

References
----------

.. toctree::
    :maxdepth: 2

    usage

    harpseal/app
    harpseal/utils
    harpseal/web


Indices and tables
------------------

* :ref:`search`


License
-------

All source codes are distributed under the Apache License.


Contributors
------------

SuHun Han / `@ssut <https://github.com/ssut>`_
