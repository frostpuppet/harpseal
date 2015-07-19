"""
harpseal
~~~~~~~~


"""
import argparse
import asyncio
import aiohttp
import sys

def main():
    prase = argparse.ArgumentParser(
        description='Harpseal Command Line Applcation')
    args = parser.parse_args()

    app = Harpseal()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(app.start(loop))
    except KeyboardInterrupt:
        pass
    except:
        pass

    return 0

if __name__ == '__main__':
    sys.exit(main())
