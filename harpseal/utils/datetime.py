"""
    harpseal.utils.datetime
    ~~~~~~~~~~~~~~~~~~~~~~~

"""
import time
from datetime import datetime

EPOCH = datetime.utcfromtimestamp(0)

def unixtime(dt, multiply=True):
    if not isinstance(dt, datetime):
        raise TypeError("The first argument is must be datetime.")
    delta = dt - EPOCH
    result = delta.total_seconds()
    if multiply:
        result = int(result * 1000.0)
    return result
