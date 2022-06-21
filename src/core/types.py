"""
Types bridge
Use this `types` to handle global standard type definition

Note: The Python runtime does not enforce function and variable type annotations. 
They can be used by third party tools such as type checkers, IDEs, linters, etc.
"""
from abc import ABCMeta, abstractmethod
from hexbytes import HexBytes
from typing import (
    NewType,
    Union,
    Any,
    Protocol,
    Dict,
    NamedTuple,
    TypedDict,
    Callable,
    Tuple,
    List,
)


HexStr = NewType("HexStr", str)
Hash32 = NewType("Hash32", bytes)
Primitives = Union[bytes, int, bool]

Directory = NewType("Directory", str)
URI = NewType("URI", str)
# Command = NewType("Commands", str)
CIDStr = NewType("CIDStr", str)
Endpoint = Union[URI, str]

# web3 types
Address = Union[HexStr, str]
Abi = NewType("Abi", Dict[Any, Any])
Connector = Callable[[Endpoint], Any]
Hash = Union[HexBytes, Hash32]
PrivateKey = Union[Address, int]
TxCall = Union[NamedTuple, TypedDict]
TxAnswer = Union[NamedTuple, TypedDict]
SignedTransaction = NewType("SignedTransaction", NamedTuple)

# ipfs types
ExecResult = TypedDict("ExecResult", {"result": Any})
RemotePin = TypedDict("PinRemote", {"status": str, "cid": str, "name": str})
Pin = TypedDict("PinLocal", {"pins": List[str]})


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
