from __future__ import annotations

"""
Types bridge "inherit" from global typing
Use this `types` to handle global standard type definition

Note: The Python runtime does not enforce function and variable type annotations.
They can be used by third party tools such as type checkers, IDEs, linters, etc.

refs:
- https://docs.python.org/3/library/typing.html#module-typing
- https://peps.python.org/pep-0544/#protocol-members
- https://google.github.io/pytype/errors.html#bad-return-type

"""

import os
import errno
import pathlib
import contextlib
import shutil


from hexbytes import HexBytes
from abc import ABCMeta, abstractmethod

# "inherit" from global typing
from typing import *  # type: ignore

# https://docs.python.org/3/library/typing.html#typing.TypeVar
T = TypeVar("T")

HexStr = NewType("HexStr", str)
Hash32 = NewType("Hash32", bytes)
Primitives = Union[bytes, int, bool]
Hash = Union[HexBytes, Hash32]

ID = NewType("ID", str)
CID = NewType("CID", str)
Raw = NewType("Raw", Mapping[str, Any])
URI = NewType("URI", str)
Endpoint = Union[URI, str]


class Command(Protocol, metaclass=ABCMeta):
    """Command specify needed methods for commands execution."""

    @abstractmethod
    def __call__(self) -> Any:
        """Call exec the command.
        Each command procedure should be implemented here.

        :return: Any data returned by command executor
        :rtype: Any
        """
        ...

    @abstractmethod
    def __str__(self) -> str:
        """How to represent your command as string?"""
        ...


class Path(str):

    """Enhanced string type extended with features needed to handle paths"""
    
    
    def __getattr__(self, name: str):
        """Proxy handling pathlib features"""
        return getattr(pathlib.Path(self), name)

    def make(self) -> Path:
        """Enhanced path mkdir

        :param dir_: dir to create
        :return: string new created dir
        :rtype: str
        """
        dirname = os.path.dirname(self)
        Path(dirname).mkdir(parents=True, exist_ok=True)
        return Path(dirname)

    def extension(self) -> str:
        """Extract file extension

        :param file: file path
        :return: extension
        :rtype: str
        """

        _, file_extension = os.path.splitext(self)
        file_extension = file_extension.replace(".", "")
        return file_extension

    def copy(self, output: Path) -> Path:
        """Copy file from origin to output dir.
        If output directory does'nt exists it will be created.

        :param origin: file path
        :param output: destination directory
        :return: new absolute file path
        :type: Directory
        """

        self.make()  # make the path if doesn't exists
        # copy the file to recently created directory
        path = shutil.copy(self, output)
        return Path(path)

    @contextlib.contextmanager
    def read(self) -> Iterator[str]:
        """Return file content.
        If file is not found, exception is raised.

        :param dir_: file path
        :return: file content
        :rtype: Iterator[str]
        :raises FileNotFoundError: if file does not exist
        """

        # Lets ensure that the database file exists
        if not self.exists():  # Check if path exist if not raise error
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self)

        with self.open() as file:
            content = file.read()
            file.close()  # don't leak a file descriptor
            yield content
