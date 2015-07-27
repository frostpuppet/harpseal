Creating plugins
================

0. Restrictions
---------------

There is some restrictions on the create of the Plugin.

* All plugin executions should not be blocked by any conditions. If so, it would block the event-loop and carries ability to disturb the other plugins and the web service.

* All plugins have to pass all variables that is defined in the plugin initialization.

1. Decide which field types to use
----------------------------------

You can use several types of graph that are currently available only the following:

* ``line``: `Line Graph <http://www.amcharts.com/demos/line-with-custom-bullets>`_.
* ``stack``: `Stacked Column Chart <http://www.amcharts.com/demos/stacked-column-chart>`_.
* ``full-stack``: `100% stacked Column Chart <http://www.amcharts.com/demos/100-stacked-column-chart>`_.
* ``bar``: `Simple Column Chart <http://www.amcharts.com/demos/simple-column-chart>`_.

2. Let's write a plugin script
------------------------------

.. code-block:: python

   import asyncio
   from harpseal.plugin import Plugin

   class YourPlugin(Plugin):
       name = '(required) your-plugin-name' # The plugin name should be in alphabet, numberals and underline(_) only.
       description = '(required) plugin description here'
       priority = 0  # not implemented yet
       every = 1  # every 1 minute. although it is not recommended to set this value in float, it's just okay.

       def init(self):
           # graph type definitions
           self.field_types['a'] = 'line'
           self.field_types['b'] = 'stack'
           self.field_types['c'] = 'full-stack'
           # field type definitions (`int` or `float`)
           # one tuple(`()`) per one legend
           self.fields['a'] = [('normal', int, ), ('abnormal', int, ), ]
           self.fields['b'] = [('normal', float, ), ('abnormal', float, ), ]
           self.fields['c'] = [('normal', float, ), ('abnormal', float, ), ]

       @asyncio.coroutine
       def provider(self):  # data provider
           data = self.data_form()
           data['a'].set('normal', 100)
           data['a'].set('abnormal', 150)
           # ...
           return data

-. The parent plugin class
--------------------------

.. autoclass:: harpseal.plugin.Plugin
    :members:
    :undoc-members:
    :show-inheritance:
