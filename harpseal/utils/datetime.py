"""
    harpseal.utils.datetime
    ~~~~~~~~~~~~~~~~~~~~~~~

"""
import time
from datetime import datetime, timedelta

EPOCH = datetime.utcfromtimestamp(0)

def unixtime(dt, multiply=True):
    if not isinstance(dt, datetime):
        raise TypeError("The first argument is must be datetime.")
    delta = dt - EPOCH
    result = delta.total_seconds()
    if multiply:
        result = int(result * 1000.0)
    return result

def ago(**kwargs):
    dt = datetime.now() - timedelta(**kwargs)
    return dt

def parse(text, fmt=r'%Y-%m-%d'):
    num = None
    dt = None
    try:
        num = int(text)
    except:
        pass
    else:
        if len(text) == 13:
            num /= 1000
        dt = datetime.fromtimestamp(num)
    if not dt:
        if fmt == r'%Y-%m-%d' and ' ' in text:
            count = text.count(':') + 1
            adds = ':'.join([r'%H', r'%M', r'%S'][:count])
            fmt = '{} {}'.format(fmt, adds)
        dt = datetime.strptime(text, fmt)

    return dt
