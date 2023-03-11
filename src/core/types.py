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
import cid  # type: ignore
import pathlib
import contextlib
import shutil
import urllib.parse as parse

from dataclasses import dataclass
from hexbytes import HexBytes
from abc import ABCMeta, abstractmethod, ABC

# "inherit" from global typing
from typing import *  # type: ignore

# https://docs.python.org/3/library/typing.html#typing.TypeVar
T = TypeVar("T")
C = TypeVar("C", contravariant=True)

JSON = Dict[Any, Any]
Raw = NewType("Raw", Mapping[str, Any])
HexStr = NewType("HexStr", str)
Hash32 = NewType("Hash32", bytes)
Primitives = Union[bytes, int, bool]
Hash = Union[HexBytes, Hash32]


@dataclass
class StdOut:
    exit_code: int
    output: Any


class Proxy(Protocol, Generic[C], metaclass=ABCMeta):
    """This protocol pretends to enforce proxy calls to underlying methods

    eg.
        # Contract can be any based on lib
        # Every network lib expose in a different way the programmatic call to functions.

        # using Web3
        c = Contract()

        # We don't know the accessor for functions for every lib
        c.functions.mint() <- how can we handle `mint` for any different lib?

        # So...
        # probably we need an standard interface here to delegate calls?

        c = Contract()
        c.mint() # Does'nt matter how the call is made underneath

    """

    @abstractmethod
    def __init__(self, interface: C):
        """Interface may be anything but MUST expose a subscriptable object to handle it"""
        ...

    @abstractmethod
    def __getattr__(self, name: str) -> Callable[[Any], Any]:
        """Control behavior for when a user attempts to access an attribute that doesn't exist.
        This method delegate the call to any underlying tool or library.

        :return: expected method to call
        :rtype: Callable[[Any], Any]
        """
        ...


class Adapter(ABC, Generic[T]):
    """Adapter template that specifies behavior for classes that can extend and interchange its implementation.
    Such an interface is expected to be adapted from an underlying library."""

    _input: T
    _name: str

    def __init__(self, name: str, input: T):
        """Initialize a new instance with bound library and name"""
        self._input = input
        self._name = name

    def __str__(self):
        """String representation for library"""
        return self._name

    def __instancecheck__(self, instance: T):
        """Pass instance checking to underlying interface."""
        return isinstance(instance, self._input.__class__)

    def __call__(self, instance: T):
        """Allow chaining to control the fluent interface keeping object reference.

        :param interface: the interface to chain
        :return: None
        :rtype: None
        """
        self._input = instance

    @abstractmethod
    def __getattr__(self, name: str) -> Callable[[Any], Any]:
        """Control behavior for when a user attempts to access an attribute that doesn't exist.
        This method delegate the call to any underlying tool or library.

        :return: expected method to call
        :rtype: Callable[[Any], Any]
        """
        ...


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


class _ExtensibleStr(str):
    def __new__(cls, value: str, *args: Any, **kwargs: Any):
        # explicitly only pass value to the str constructor
        return super().__new__(cls, value)


class CID(_ExtensibleStr):
    """Enhanced bridge string type extended with features needed to handle CIDs"""

    _cid: Union[cid.CIDv0, cid.CIDv1]

    def __init__(self, *args: Any, **kwargs: Any):
        try:
            self._cid = cid.from_string(self)  # type: ignore
        except ValueError:
            # we want to allow control the behavior using `valid` method
            ...

    def __getattr__(self, name: str) -> Any:
        if not self._cid:
            raise AttributeError(name)
        return getattr(self._cid, name)

    def valid(self) -> bool:
        return cid.is_cid(self)  # type: ignore

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        if not cls(v).valid():
            raise ValueError("string must be a CID")


class URL(_ExtensibleStr):
    """Enhanced bridge string type extended with features needed to handle urls
    ref: https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse
    """

    _parsed: parse.ParseResult

    def __init__(self, *args: Any, **kwargs: Any):
        try:
            self._parsed = parse.urlparse(self)
        except ValueError:
            # we want to allow control the behavior using `valid` method
            ...

    def __getattr__(self, name: str) -> str:
        if not self._parsed:
            raise AttributeError(name)
        return getattr(self._parsed, name)

    def valid(self) -> bool:
        allowed_schemes = {"http", "https"}
        valid_scheme = self.scheme in allowed_schemes
        return all((valid_scheme, self.netloc))

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        if not cls(v).valid():
            raise ValueError("string must be a URL")


class Path(_ExtensibleStr):

    """Enhanced bridge string type extended with features needed to handle paths"""

    _path: pathlib.Path

    def __init__(self, *args: Any, **kwargs: Any):
        self._path = pathlib.Path(self)

    def __getattr__(self, name: str) -> Any:
        """Proxy handling pathlib features"""
        if name == "__setstate__":
            # pickle avoid recursion
            raise AttributeError(name)
        return getattr(self._path, name)

    def make(self) -> Path:
        """Enhanced path mkdir

        :param dir_: dir to create
        :return: string new created dir
        :rtype: str
        """
        dirname = os.path.dirname(self)
        path = Path(dirname)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def extension(self) -> str:
        """Extract file extension

        :param file: file path
        :return: extension
        :rtype: str
        """

        file_extension = self._path.suffix
        file_extension = file_extension.replace(".", "")
        return file_extension

    def copy(self, output: Path) -> Path:
        """Copy file from origin to output dir.

        :param origin: file path
        :param output: destination directory
        :return: new absolute file path
        :type: Directory
        """

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
        """

        with self.open() as file:
            content = file.read()
            file.close()  # don't leak a file descriptor
            yield content

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        if not cls(v).exists():
            raise ValueError("string must be a Path")
