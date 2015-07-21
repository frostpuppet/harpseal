"""
    harpseal.plugin
    ~~~~~~~~~~~~~~~

    Plugin class definition

"""
import asyncio

class Plugin(object):
    """
    Base plugin model
    """
    name = ''
    description = ''
    priority = 0
    every = 1

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
            raise ValueError("You must set the variables for both 'name' and 'description'.")
        properties = {
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
            'every': self.every,
        }
        return properties
