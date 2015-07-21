"""
    harpseal.plugin
    ~~~~~~~~~~~~~~~

    Plugin class definition

"""
import asyncio

from harpseal.utils.commands import execute

class Plugin(object):
    """
    Base plugin model
    """
    name = ''
    description = ''
    priority = 0
    every = 1

    _app = None

    @asyncio.coroutine
    def execute(self):
        """
        Execute plugin
        """
        if self.provider.__name__ != 'coroutine':
            raise TypeError("You must wrap the function with '@asyncio.coroutine' decorator.")
        data = yield from self.provider()
        if data is None:
            raise AssertionError("The data is not passed from the .provider() function.")

    @asyncio.coroutine
    def _call(self, command):
        """
        Execute a command on the event-loop and then return the result when finished.
        """
        if Plugin._app is None:
            raise AssertionError("The property ._app is not assigned.")
        result = yield from execute(Plugin._app, command)
        return result

    @asyncio.coroutine
    def provider(self):
        """
        Plugin provider that returns a plugin's result.
        """
        raise NotImplementedError(".provider() must be overridden.")

    @property
    def properties(self):
        """
        Return the instance properties as a dict.
        """
        if self.name == '' or self.description == '':
            raise ValueError("You must set the variables for both .name and .description.")
        properties = {
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
            'every': self.every,
        }
        return properties
