from __future__ import annotations

import asyncio


from abc import abstractmethod, ABCMeta
from src.core.types import Protocol, StdOut

SubProcess = asyncio.subprocess.Process
Reader = asyncio.StreamReader
Loop = asyncio.BaseEventLoop


class IPC(Protocol, metaclass=ABCMeta):
    """Inter-process communication.
    IPC exchange I/O between main process and sub processes.
    Collect logs and subprocess status.
    """

    _cmd: str
    _loop: Loop
    _stream: Reader

    @abstractmethod
    def __init__(self, cmd: str):
        ...

    @abstractmethod
    async def pipe(self, data: bytes) -> StdOut:
        """Check the output and analyze it.
        Failed if capture ERROR logs or stderr pipe.

        :return: standard output
        :rtype: StdOut
        """

        # start process and check return code
        ...

    @abstractmethod
    async def _run(self) -> SubProcess:
        """Initialize subprocess call.
        We use a custom factory to stream process output.

        :return: subprocess instance
        :rtype: SubProcess
        """

        # execute nodejs command and communicate the data input
        ...

    @abstractmethod
    def communicate(self, data: bytes) -> StdOut:
        """Communicate with process

        :param data: message sent to process
        :return: resulting output
        :rtype: Any
        """
        ...
