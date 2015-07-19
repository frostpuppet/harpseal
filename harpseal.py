"""
harpseal
~~~~~~~~


"""
import argparse
import asyncio
import sys

from harpseal.app import Harpseal

def main():
    parser = argparse.ArgumentParser(
        description='Harpseal Command Line Applcation')
    args = parser.parse_args()

    app = Harpseal()

    retcode = 0
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(app.start(loop))
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        retcode = 1
        print(exc)

    return retcode

if __name__ == '__main__':
    sys.exit(main())
