from __future__ import annotations

import asyncio
from abc import ABCMeta, abstractmethod
from src.core.types import Iterator, Any


Reader = asyncio.StreamReader
Loop = asyncio.BaseEventLoop


class ProtocolTracer(asyncio.subprocess.SubprocessStreamProtocol, metaclass=ABCMeta):
    """Like StreamReaderProtocol, but for a subprocess.
    ref: https://docs.python.org/3.6/library/asyncio-stream.html
    """

    _reader: Reader

    def __init__(self, reader: Reader, limit: int, loop: Loop):
        super().__init__(limit=limit, loop=loop)
        self._reader = reader

    def __str__(self) -> str:
        """Return full captured logs from subprocess."""
        ...

    def __iter__(self) -> Iterator[str]:
        """Return iterator with subprocess logs lines."""
        ...

    def pipe_data_received(self, fd: int, data: bytes | str):
        """Called when the child process writes data into its stdout or stderr pipe."""
        # TODO intercept ERR logs
        ...

    def pipe_connection_lost(self, fd: int, exc: Any):
        """Called when one of the pipes communicating with the child process is closed."""
        # TODO intercept unexpected
        ...
        
    def process_exited(self):
        # TODO intercept here the exist status

        ...

    @abstractmethod
    def pipe(self):
        """Stream output from process"""
        
    
    @abstractmethod
    def fault_detected(self) -> bool:
        """Check if the process failed.
        Failed if capture exit status > 0, ERROR logs or stderr pipe.

        :return: If process failed True is returned otherwise False.
        :rtype: bool
        """

        ...
