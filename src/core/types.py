"""
Types bridge "inherit" from global typing
Use this `types` to handle global standard type definition

Note: The Python runtime does not enforce function and variable type annotations. 
They can be used by third party tools such as type checkers, IDEs, linters, etc.
"""
from hexbytes import HexBytes
from abc import ABCMeta, abstractmethod
# "inherit" from global typing
from typing import * # type: ignore

HexStr = NewType("HexStr", str)
Hash32 = NewType("Hash32", bytes)
Primitives = Union[bytes, int, bool]
Hash = Union[HexBytes, Hash32]

ID = str
CIDStr = str
Directory = str
URI = NewType("URI", str)
Endpoint = Union[URI, str]


class Subscriptable(Protocol):
    """
    Subscriptable definition to enforce dynamic properties accessor
    """

    def __getattr__(self, name: str) -> Any:
        ...


class Container(Protocol, metaclass=ABCMeta):
    """
    Docker container abstraction adapted from docker lib
    """

    @abstractmethod
    def exec_run(self, cmd: str) -> Tuple[bool, bytes]:
        ...


class Command(Protocol, metaclass=ABCMeta):
    """
    Interface definition for command execution.
    """

    @abstractmethod
    def __call__(self) -> Any:
        """
        Call exec command execution based on params.
        Define your call using sandbox param.

        :param sandbox: pass the executor to call or where the command will run
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
