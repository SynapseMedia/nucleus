import asyncio
import functools
import os
import re
import subprocess

from nucleus.core.types import List, Sequence, Union

from .constants import EXIT_FAILURE, EXIT_SUCCESS
from .protocol import StreamProtocol
from .types import Loop, Reader, StdOut, SubProcess


def _decode_bytes(b: bytes) -> str:
    """Helper function to decode bytes to string

    :param b: bytes to decode
    :return: string decoded
    :rtype: str
    """
    return b.decode()


def _match_faulty_line(lines: Sequence[str]) -> Union[str, None]:
    """Check if the process failed.
    Consideration: Is Faulty if capture ERROR logs.

    :param line: input line to analyze
    :return: if process failed True is returned otherwise False.
    :rtype: str | None
    """

    for line in lines:
        # try find a fault in log lines
        pattern = r'(\w+)?(Error|\[ERROR\])'  # what should we find?
        match_found = re.search(pattern, line)
        if match_found:
            return line

    return None


async def _trace(stream: Reader) -> StdOut:
    """Async pluggable function to trace information from process stream

    :param stream: read stream
    :return: standard output
    :rtype: StdOut

    """

    logs: List[str] = []

    async for lines in stream:
        raw_lines = lines.split(b'\n')
        decoded_lines = map(_decode_bytes, raw_lines)
        cleaned_lines = tuple(filter(len, decoded_lines))
        match_found = _match_faulty_line(cleaned_lines)

        if match_found:
            # even if the process do not exit with failure,
            # we can force return as failure if we find a fault error.
            return StdOut(EXIT_FAILURE, iter((match_found,)))

        # concat good logs
        logs += cleaned_lines

    # parse list of logs to lazy iterator
    return StdOut(EXIT_SUCCESS, iter(logs))


class IPC:
    """Inter-process communication.
    IPC exchange I/O between main process and sub processes.
    Collect logs and subprocess status.
    """

    _cmd: str
    _loop: Loop
    _stream: Reader

    def __init__(self, cmd: str):
        self._cmd = cmd
        self._loop = asyncio.get_event_loop()  # type: ignore
        self._stream = Reader(loop=self._loop)

    def stream(self):
        """If we need to read live the output we can get stream directly using this method

        :return: stream reader
        :rtype: Reader
        """
        return self._stream

    async def pipe(self, data: bytes) -> StdOut:
        """Check the output and analyze it.
        Failed if capture ERROR logs or stderr pipe.

        :return: standard output
        :rtype: StdOut
        """

        # start process and check return code
        proc = await self._run()
        if proc.returncode:
            return StdOut(proc.returncode, iter([]))

        tasks = (proc.communicate(data), _trace(self._stream))
        (_, result) = await asyncio.gather(*tasks)
        return result

    async def _run(self):
        """Initialize subprocess call.
        We use a custom factory to stream process output.

        :return: subprocess instance
        :rtype: SubProcess
        """

        # execute nodejs command and communicate the data input
        protocol_factory = functools.partial(StreamProtocol, self._stream, loop=self._loop)

        # run the cmd shell command + return a Process instance.
        transport, protocol = await self._loop.subprocess_shell(
            protocol_factory,
            self._cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            env=os.environ.copy(),
        )

        return SubProcess(transport, protocol, self._loop)

    def communicate(self, data: bytes = b'') -> StdOut:
        """Communicate with process

        :param data: message sent to process
        :return: resulting output
        :rtype: Any
        """
        routine = asyncio.gather(self.pipe(data))
        (result,) = self._loop.run_until_complete(routine)
        return result
