"""
    harpseal.models
    ~~~~~~~~~~~~~~~

    Mongo models
"""

from datetime import datetime

from mongoengine import *

__all__ = ['make_model']

class BaseModel(DynamicDocument):
    """
    BaseModel for harpseal models
    """

    created_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

def make_model(name, args):
    """
    Create a new model with given name and arguments
    """
    cls = type(name, (BaseModel, ), {'__init__': __init__})
    for arg in args:
        if arg[1] is int:
            field = LongField()
        elif arg[1] is float:
            field = FloatField()
        else:
            continue
        setattr(cls, arg[0], field)
    return cls
