import asyncio

# Convention for importing types
from nucleus.core.types import Any

from .constants import FILE_NO
from .types import Loop, Reader


class StreamProtocol(asyncio.subprocess.SubprocessStreamProtocol):
    """Like StreamReaderProtocol, but for a subprocess.
    ref: https://docs.python.org/3.6/library/asyncio-stream.html
    """

    _reader: Reader

    def __init__(self, reader: Reader, loop: Loop, limit: int = 2**6):
        super().__init__(limit=limit, loop=loop)
        self._reader = reader

    def pipe_data_received(self, fd: int, data: Any):
        """Called when the child process writes data into its stdout or stderr pipe.

        fd: the integer file descriptor of the pipe.
        data: non-empty bytes object containing the received data.
        """
        super().pipe_data_received(fd, data)
        if fd in FILE_NO:
            self._reader.feed_data(data)

    def pipe_connection_lost(self, fd: int, exc: Any):
        """Called when one of the pipes communicating with the child process is closed.

        fd: the integer file descriptor of the pipe.
        exc: exception if exists else None.
        """
        super().pipe_connection_lost(fd, exc)
        if fd in FILE_NO:
            if exc is not None:
                self._reader.set_exception(exc)
                return

            # end of streaming
            self._reader.feed_eof()
