"""
Note: The Python runtime does not enforce function and variable type annotations. 
They can be used by third party tools such as type checkers, IDEs, linters, etc.
"""
from hexbytes import HexBytes
from typing import (
    NewType,
    Union,
    Any,
    TypeVar,
    Protocol,
    Dict,
    NamedTuple,
    TypedDict,
    Callable
)


# Types bridge
# Use this `types` to handle global standard type definition
# Add providers/transaction/ types based on network lib
# eg. BaseProvider for web3
HexStr = NewType("HexStr", str)
Hash32 = NewType("Hash32", bytes)

Primitives = Union[bytes, int, bool]
TxCall = Union[NamedTuple, TypedDict]
TxAnswer = Union[NamedTuple, TypedDict]

# Aliases
Hash = Union[HexBytes, Hash32]
Address = Union[HexStr, str]
PrivateKey = Union[Address, int]

SignedTransaction = NewType("SignedTransaction", NamedTuple)
Directory = NewType("Directory", str)
Command = NewType("Commands", str)
Uri = NewType("URI", str)
Abi = NewType("Abi", Dict[Any, Any])

CidStr = NewType("CIDStr", str)
Endpoint = Union[Uri, str]
Connector = Callable[[Endpoint], Any]

# By convention var types should start with "T" followed by type name
T = TypeVar("T")


class Subscriptable(Protocol):
    def __getattr__(self, name: str) -> Any:
        ...
