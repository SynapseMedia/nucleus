"""
Types bridge "inherit" from global typing
Use this `types` to handle global standard type definition

Note: The Python runtime does not enforce function and variable type annotations. 
They can be used by third party tools such as type checkers, IDEs, linters, etc.
"""
from hexbytes import HexBytes
from abc import ABCMeta, abstractmethod

# "inherit" from global typing
from typing import *  # type: ignore

HexStr = NewType("HexStr", str)
Hash32 = NewType("Hash32", bytes)
Primitives = Union[bytes, int, bool]
Hash = Union[HexBytes, Hash32]

ID = str
CIDStr = str
Directory = str
URI = NewType("URI", str)
Endpoint = Union[URI, str]


class Printable(Protocol, metaclass=ABCMeta):
    """Printable abstraction to enforce implement string representation methods."""

    @abstractmethod
    def __str__(self) -> str:
        """
        Human readable string representation for abstraction.
        """
        ...


class Accessor(Protocol, metaclass=ABCMeta):
    """
    Accessor abstraction to enforce dynamic properties.
    You can define behavior for when a user attempts to access an attribute that doesn't exist.
    """

    @abstractmethod
    def __getattr__(self, name: str) -> Any:
        """
        Dynamic access to an attribute.
        Here should be handled the logic for dynamic attribute access.

        :param name: The name of the attribute
        :return: Any data processed using the attribute
        :rtype: Any
        """
        ...


class Command(Protocol, metaclass=ABCMeta):
    """Command specify needed methods for commands execution."""

    @abstractmethod
    def __call__(self) -> Any:
        """
        Call exec the command.
        Each command procedure should be implemented here.

        :return: Any data returned by command executor
        :rtype: Any
        """
        ...

    @abstractmethod
    def __str__(self) -> str:
        """
        How to represent your command as string?
        """
        ...
