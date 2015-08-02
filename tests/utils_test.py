import asyncio
from datetime import datetime, timedelta

from pytest import mark, raises

from harpseal.utils import commands
from harpseal.utils import datetime as dtutils

def test_commands():
    @asyncio.coroutine
    def test(future):
        result = yield from commands.execute('pwd')
        future.set_result(result)

    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    loop.run_until_complete(test(future))
    loop.close()
    assert future.result()

@mark.parametrize('params,expected', [
    ([datetime.utcfromtimestamp(1437983134), True], 1437983134000),
    ([datetime.utcfromtimestamp(1437983134), False], 1437983134),
])
def test_dtutils_unixtime(params, expected):
    assert dtutils.unixtime(*params) == expected

def test_raises_dtutils_unxtime():
    with raises(TypeError):
        dtutils.unixtime(None)

def test_dtutils_ago():
    m1day = datetime.now() - timedelta(days=1)
    assert dtutils.ago(days=1).day == m1day.day

PARSE_EXPECTED = datetime(2015, 7, 27, 7, 45, 34)
@mark.parametrize('text,expected', [
    ('1437983134', PARSE_EXPECTED),
    ('1437983134000', PARSE_EXPECTED),
    ('2015-07-27', datetime(2015, 7, 27, 0, 0, 0)),
    ('2015-07-27 07', datetime(2015, 7, 27, 7, 0, 0)),
    ('2015-07-27 07:45', datetime(2015, 7, 27, 7, 45, 0)),
    ('2015-07-27 07:45:34', datetime(2015, 7, 27, 7, 45, 34)),
])
def test_dtutils_parse(text, expected):
    assert dtutils.parse(text) == expected

def test_raises_dtutils_parse():
    with raises(ValueError):
        dtutils.parse('1111111111111')
        dtutils.parse('to be failed')
