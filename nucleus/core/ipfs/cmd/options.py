from dataclasses import dataclass

from nucleus.core.exceptions import IPFSRuntimeError
from nucleus.core.types import Path


@dataclass(slots=True)
class File:
    """File represent "files" params in request based on input path.
    :raises IPFSRuntimeError if file does not exist.
    """

    path: Path

    def __post_init__(self):
        if not self.path.exists():
            raise IPFSRuntimeError(f'raised trying to execute `add` directory with an invalid path {self.path}')

    def __iter__(self):
        file_name = self.path.name
        blob = self.path.read_bytes()
        yield 'files', {'file': (file_name, blob)}


@dataclass(slots=True)
class Text:
    """Text represent "data" param in request based on input text."""

    input: bytes

    def __iter__(self):
        yield 'files', {'file': ('meta', self.input)}


__all__ = ('File', 'Text')
