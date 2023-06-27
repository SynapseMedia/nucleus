from dataclasses import dataclass

from nucleus.core.exceptions import IPFSRuntimeError
from nucleus.core.types import Path


@dataclass(slots=True)
class Dir:
    """Dir represent directory params in request based on input path.

    :raises IPFSRuntimeError: If directory does not exist.
    """

    path: Path

    def __post_init__(self):
        if not self.path.is_dir():
            raise IPFSRuntimeError(f'raised trying to execute `add` with an invalid directory {self.path}')

    def __iter__(self):
        yield 'files', [('file', (child.name, child.read_bytes())) for child in self.path.iterdir()]


@dataclass(slots=True)
class File:
    """File represent "files" params in request based on input path.

    :raises IPFSRuntimeError: If file does not exist.
    """

    path: Path

    def __post_init__(self):
        if not self.path.is_file():
            raise IPFSRuntimeError(f'raised trying to execute `add` with an invalid path {self.path}')

    def __iter__(self):
        yield 'files', {'file': (self.path.name, self.path.read_bytes())}


@dataclass(slots=True)
class Text:
    """Text represent "data" param in request based on input text."""

    input: bytes

    def __iter__(self):
        yield 'files', {'file': ('meta', self.input)}


__all__ = ('File', 'Text')
