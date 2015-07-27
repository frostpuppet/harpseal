"""
    Config parser
    ~~~~~~~~~~~~~

    Harpseal config parser based on JSON
"""
import os
import json

from harpseal.classes import Singleton

class Config(metaclass=Singleton):
    """Config parser, working like `dict`."""

    def __init__(self, path):
        if not os.path.exists(path):
            raise IOError("The path of the config file does not exist.")
        self._conf = {}
        with open(path, 'r', encoding='utf-8') as f:
            self._conf = json.loads(f.read())
        if not self._conf:
            raise IOError("Failed to load the config file or invalid JSON format.")

    def __getitem__(self, key):
        result = None
        if key in self._conf:
            result = self._conf[key]
        return result
