"""
    Models
    ~~~~~~
"""

from datetime import datetime

from mongoengine import *

from harpseal.conf import Config

__all__ = ['make_model']

class Items(DynamicEmbeddedDocument):
    pass

def make_model(name, args):
    """Create a new model with name and arguments given."""
    def add(self, **kwargs):
        items = Items(**kwargs)
        self.items = items
        self.created_at = datetime.now()

    expires = Config()['expires']
    meta = {
        'indexes': [
            {'fields': ['-created_at'], 'expireAfterSeconds': expires}
        ]
    }

    cls = type(name, (DynamicDocument, ), {'add': add, 'meta': meta})
    return cls
