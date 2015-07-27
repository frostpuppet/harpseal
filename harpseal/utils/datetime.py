"""
    DateTime Tools
    ~~~~~~~~~~~~~~

"""
import time
from datetime import datetime, timedelta

EPOCH = datetime.utcfromtimestamp(0)

def unixtime(dt, multiply=True):
    """Return the unix timestamp of the datetime given.

    :param bool multiply: whether return as 13-digit timestamp or 10-digit timestamp
    """
    if not isinstance(dt, datetime):
        raise TypeError("The first argument is must be datetime.")
    delta = dt - EPOCH
    result = delta.total_seconds()
    if multiply:
        result = int(result * 1000.0)
    return result

def ago(**kwargs):
    """Return the datetime that points specific times ago."""
    dt = datetime.now() - timedelta(**kwargs)
    return dt

def parse(text, fmt=r'%Y-%m-%d'):
    """Return the datetime of either text or integer given.
    This function automatically recognizes the format of text or integer.
    """
    num = None
    dt = None
    try:
        num = int(text)
    except:
        pass
    else:
        if len(text) == 13:
            num /= 1000
        dt = datetime.utcfromtimestamp(num)
    if not dt:
        if fmt == r'%Y-%m-%d' and ' ' in text:
            count = text.count(':') + 1
            adds = ':'.join([r'%H', r'%M', r'%S'][:count])
            fmt = '{} {}'.format(fmt, adds)
        dt = datetime.strptime(text, fmt)

    return dt
