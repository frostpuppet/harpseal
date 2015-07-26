Harpseal
--------
*Harpseal* is a python app that collects system resources, usage and others by plugins which are extendable. *Harpseal* gives you easy accessible API to draw a graph or to analysis data by JSON format.

Features
--------

* Plugin
* Spoke-hub model
* HTTP API - JSON/JSONP (callback)

Installation
------------

(TBA)

Built-in Plugins
---------------

* `cpu` - CPU watch plugin; it watches for each CPU usage, PID count and CPU times.
* `mem` - Memory watch plugin; it watches for detailed memory usage data including swap memory.
* `disk` - Disk watch plugin; it watches for each disk IOs and spaces.
* `net` - Network watch plugin; it logs for network statistics.

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

All source codes are distributed under GNU GPL 2 license.


Contributors
------------

SuHun Han / `@ssut <https://github.com/ssut>`_
