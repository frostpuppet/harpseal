"""
    Command Tools
    ~~~~~~~~~~~~~

"""
import asyncio
import shlex
from asyncio import subprocess

__all__ = ['execute']

@asyncio.coroutine
def execute(command):
    """Execute a command."""
    command = shlex.split(command)

    # Create the subprocess, redirect the standard output into a pipe
    process = yield from asyncio.create_subprocess_exec(*command, 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = yield from process.communicate()

    return stdout
