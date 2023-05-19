from __future__ import annotations

import json
import pathlib
import urllib.parse as parse
from collections import UserDict
from types import *  # noqa: F403

# "inherit" from global typing
from typing import *  # noqa: F403

from hexbytes import HexBytes
from multiformats import CID as MultiFormatCID

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


# https://docs.python.org/3/library/typing.html#typing.TypeVar
T = TypeVar('T')
T_contra = TypeVar('T_contra', contravariant=True)
T_co = TypeVar('T_co', covariant=True)

Raw = Dict[Any, Any]
ExceptionType = Type[Exception]
HexStr = NewType('HexStr', str)
Hash32 = NewType('Hash32', bytes)
Primitives = Union[bytes, int, bool]
Hash = Union[HexBytes, Hash32]
Func = Callable[..., Any]
Dynamic = SimpleNamespace
Setting = Iterator[Tuple[str, Any]]


class Settings(Protocol):
    """Setting defines the expected behavior of any configuration parameters.
    Use this class to create setting subtypes.
    """

    def __iter__(self) -> Setting:
        """Yield key value pair to build compilation of arguments.
        Allow to convert setting as dict.
        """
        ...


class _ExtensibleStr(str):
    def __new__(cls, value: str):
        # explicitly only pass value to the str constructor
        return super().__new__(cls, value)

    def __deepcopy__(self, *_: Any):
        """Override deep copy to avoid serialization error with underlying object"""
        return self


class CID(_ExtensibleStr):
    """Enhanced bridge string type extended with features needed to handle CIDs
    ref: https://multiformats.readthedocs.io/en/latest/cid.html
    """

    _cid: MultiFormatCID

    def __init__(self, value: str):
        try:
            # a CID is always a CID, so if it's not valid, it simply can't be one
            # raise an exception if an invalid CID is passed
            self._cid = MultiFormatCID.decode(value)
        except (ValueError, KeyError) as e:
            raise ValueError(str(e))

    def format(self) -> MultiFormatCID:
        """Return internal CID object"""
        return self._cid

    def __bytes__(self):
        return bytes(self._cid)

    def __getattr__(self, name: str) -> Any:
        """Proxy handling CID features"""
        return getattr(self._cid, name)

    @classmethod
    def create(cls, *args: Any, **kwargs: Any):
        return cls(str(MultiFormatCID(*args, **kwargs)))


class URL(_ExtensibleStr):
    """Enhanced bridge string type extended with features needed to handle urls
    ref: https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse
    """

    _parsed: parse.ParseResult

    def __init__(self, value: str):
        self._parsed = parse.urlparse(value)

    def __getattr__(self, name: str) -> str:
        """Proxy handling urlparse features"""
        return getattr(self._parsed, name)

    def valid(self) -> bool:
        allowed_schemes = {'http', 'https'}
        valid_scheme = self.scheme in allowed_schemes
        # contains a valid scheme and valid domain
        # ref: https://docs.python.org/3/library/urllib.parse.html
        return all((valid_scheme, self.netloc))

    @classmethod
    def __get_validators__(cls):
        """Add compat with pydantic validators"""
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        if not cls(v).valid():
            raise ValueError('string must be a URL')


class Path(_ExtensibleStr):

    """Enhanced bridge string type extended with features needed to handle paths"""

    _path: pathlib.Path

    def __init__(self, value: str):
        self._path = pathlib.Path(value)

    def __getattr__(self, name: str) -> Any:
        """Proxy handling pathlib features"""
        return getattr(self._path, name)

    def size(self):
        """Shortcut for Path.size().st_size"""
        return self.stat().st_size

    @classmethod
    def __get_validators__(cls):
        """Add compat with pydantic validators"""
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        if not cls(v).exists():
            raise ValueError('string must be a Path')


class JSON(UserDict[Any, Any]):

    """Enhanced bridge dict type extended with features needed to handle json structure"""

    def __str__(self) -> str:
        """Return json as json string"""
        return json.dumps(dict(self))

    def __bytes__(self) -> bytes:
        """Return json as bytes"""
        return bytes(str(self), 'utf-8')

    def parse(self):
        return json.loads(str(self))

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
