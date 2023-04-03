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

import json
import cid  # type: ignore
import pathlib
import urllib.parse as parse

from collections import UserDict
from hexbytes import HexBytes

# "inherit" from global typing
from typing import *  # type: ignore
from types import *  # type: ignore

# https://docs.python.org/3/library/typing.html#typing.TypeVar
T = TypeVar("T")
T_contra = TypeVar("T_contra", contravariant=True)
T_co = TypeVar("T_co", covariant=True)

ExceptionType = Type[Exception]
HexStr = NewType("HexStr", str)
Hash32 = NewType("Hash32", bytes)
Primitives = Union[bytes, int, bool]
Hash = Union[HexBytes, Hash32]
Preset = Iterator[Tuple[str, Any]]
Func = Callable[..., Any]


class Setting(Protocol):
    """Setting defines the expected behavior of any configuration parameters.
    Use this class to create setting subtypes.
    """

    def __iter__(self) -> Preset:
        """Yield key value pair to build compilation of arguments.
        Allow to convert setting as dict.
        """
        ...


class _ExtensibleStr(str):
    def __new__(cls, value: str):
        # explicitly only pass value to the str constructor
        return super().__new__(cls, value)


class CID(_ExtensibleStr):
    """Enhanced bridge string type extended with features needed to handle CIDs"""

    _cid: Union[cid.CIDv0, cid.CIDv1]

    def __init__(self, value: str):
        try:
            self._cid = cid.from_string(value)  # type: ignore
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

    def __init__(self, value: str):
        try:
            self._parsed = parse.urlparse(value)
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
        # contains a valid scheme and valid domain
        # ref: https://docs.python.org/3/library/urllib.parse.html
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

    def __init__(self, value: str):
        self._path = pathlib.Path(value)

    def __getattr__(self, name: str) -> Any:
        """Proxy handling pathlib features"""
        if name == "__setstate__":
            # pickle avoid recursion
            raise AttributeError(name)
        return getattr(self._path, name)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        if not cls(v).exists():
            raise ValueError("string must be a Path")

        ...


class JSON(UserDict[Any, Any]):

    """Enhanced bridge dict type extended with features needed to handle json structure"""

    def write(self, path: Path):
        """Create an output json file into output file with self

        :param path: directory to store json file
        :return: path to file
        :rtype: Path
        """
        json_string = json.dumps(self.data, ensure_ascii=False)
        path.write_text(json_string)
        return path

    @classmethod
    def read(cls, path: Path):
        """Read a json file and return a JSON object

        :param path: the path to read json raw
        :return: JSON
        :rtype: JSON
        """
        raw = path.read_text()
        dict = json.loads(raw)
        return cls(**dict)
