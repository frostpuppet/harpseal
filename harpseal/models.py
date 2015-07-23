"""
    harpseal.models
    ~~~~~~~~~~~~~~~

    Mongo models
"""

from datetime import datetime

from mongoengine import *

__all__ = ['make_model']

class Items(DynamicEmbeddedDocument):
    pass

def make_model(name, args):
    """
    Create a new model with given name and arguments
    """
    def add(self, **kwargs):
        items = Items(**kwargs)
        self.items = items
        self.created_at = datetime.now()

    cls = type(name, (DynamicDocument, ), {'add': add})
    return cls
