"""
    Command Tools
    ~~~~~~~~~~~~~

"""
import asyncio
import shlex

__all__ = ['execute']

class DateProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future):
        self.exit_future = exit_future
        self.output = bytearray()

    def pipe_data_received(self, fd, data):
        self.output.extend(data)

    def process_exited(self):
        self.exit_future.set_result(True)

@asyncio.coroutine
def execute(app, command):
    """Execute a command."""
    command = shlex.split(command)
    exit_future = asyncio.Future()

    # Create the subprocess controlled by the protocol DataProtocol,
    # redirect the standard output into a pipe
    process = app.loop.subprocess_exec(lambda: DataProtocol(exut_future),
                                       *command, stdin=None, stderr=None)
    transport, protocol = yield from process

    # Wait for the subprocess exit using the process_exited() method
    # of the protocol
    yield from exit_future

    # Close the stdout pipe
    transport.close()

    # Read the output which was collected by the pipe_data_received()
    # method of the protocol
    data = bytes(protocol.output)
    return data.decode('ascii').rstrip()
