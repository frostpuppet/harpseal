Harpseal API
============

This page introduces you a way to access to your harpseal API server.


1. Check your settings
----------------------

You must check your settings before you can be assigned access right. (This file might be located in ``harpseal/config.json``)

.. code-block:: json
   
   {
       "server": {
           "host": "0.0.0.0",
           "port": "24680",
           "key": "",
           "allows": [
               "127.0.0.1"
           ]
       }
   }

* **host**

  * ``127.0.0.1`` is normally the IP address assigned to be the "loopback" or local-only interface. ``localhost`` is the same as ``127.0.0.1``. — This can only communicate within the same host.

  * ``0.0.0.0`` means "listen on every available network interface", so with this can allow you communicate effectively with others.

* **port**

  * This is a number of ways to communicate with application.

  * The default port is ``24680`` as shown above.

* **key**

  * If you set this value, it will cause you to ask this key when you try to access to the API.

  * The **key** can be passed as a HTTP GET parameter ``key``.

  * The default value is not set.

* **allows**

  * This list contains IPv4 addresses that belong to the subnet. For more details regarding subnets, refer to `Subnetwork <https://en.wikipedia.org/wiki/Subnetwork>`_.

  * If you want to allow 0.0.0.0 to 255.255.255.255, just use the following subnet format: ``0.0.0.0/1``.


2. API Restrictions
-------------------

* This API does not provide security in itself without the written authorization by the above, therefore please be aware off security issues.

* If you want to get the raw values, don't use API then access MongoDB directly instead.

* The default data look up period is 7 days, you can change this with parameters.


3. Getting access to the API
----------------------------

.. warning::

   The requests may carry substantial cost implications when you request a large amount of data.

Parameters
~~~~~~~~~~

* Compare with **creation time** that expresses when the data has been added.

  * ``gte``: greater than or equal to

  * ``lte``: less than or equal to

  * format: `YYYY-mm-dd`, `YYYY-mm-dd HH`, `YYYY-mm-dd HH:MM`, `YYYY-mm-dd HH:MM:SS` or `unix timestamp` (10-digit or 13-digit)

Common Response Format
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
       "ok": true
   }

The **ok** value means that whether the request was successful or failure, this value will vary for each request.

1. Get plugin list
~~~~~~~~~~~~~~~~~~

Request: **GET** ``/plugins/list``

Response:

.. code-block:: json

   {
       "plugin name": {
           "description": "plugin description",
           "every": "plugin execution cycle in integer",
           "lastExecutedResult": "last executed result in boolean",
           "lastExecutedAt": "last executed time in unix time"
       }
   }


2. Get plugin logs
~~~~~~~~~~~~~~~~~~

Request: **GET** ``/plugins/<plugin-name>``

Response:

.. code-block:: json

   {
       "name": "plugin name",
       "description": "plugin description",
       "every": "plugin execution cycle in integer",
       "data": {
           "field": {
               "type": "graph type to draw (line, stack, full-stack, bar)",
               "legends": [
                   "created",
                   "field1",
                   "field2"
               ],
               "data": [
                   ["unixtime", "field1 value in integer or float", "field2 value in integer or float"],
                   ["unixtime", "field1 value in integer or float", "field2 value in integer or float"],
                   ["unixtime", "field1 value in integer or float", "field2 value in integer or float"]
               ]
           }
       }
   }


3. Get all plugin logs
~~~~~~~~~~~~~~~~~~~~~~

Request: **GET** ``/plugins/all``

Response:

.. code-block:: json

   {
       "data": {
           "plugin-name": {
               "description": "plugin description",
               "every": "plugin execution cycle in integer",
               "lastExecutedResult": "last executed result in boolean",
               "lastExecutedAt": "last executed time in unix time",
               "data": {
                   "field": {
                       "type": "graph type to draw (line, stack, full-stack, bar)",
                       "legends": [
                           "created",
                           "field1",
                           "field2"
                       ],
                       "data": [
                           ["unixtime", "field1 value in integer or float", "field2 value in integer or float"],
                           ["unixtime", "field1 value in integer or float", "field2 value in integer or float"],
                           ["unixtime", "field1 value in integer or float", "field2 value in integer or float"]
                       ]
                   }
               }
           }
       }
   }

4. WebSocket Support
--------------------

You can use websocket methods by accessing the url ``/``.

The request format is as follows:

.. code-block:: json

   {
       "request": "handler-name",
       "params": {}
   }


* The **handler-name** means the method name of :class:`harpseal.web.handler.Handler` which contains ``_handler`` in its name.
* Params can contain HTTP parameters which are obtained as above such as ``key`` or ``gte``.
* If you want to pass the *name* of the plugin, you'll have to add ``name`` into your JSON to be able to identify plugin.
