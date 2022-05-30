from hexbytes import HexBytes
from web3.providers.base import BaseProvider
from ffmpeg_streaming import Formats  # type: ignore
from typing import (
    NewType,
    Union,
    Any,
    Type,
    TypeVar,
    Protocol,
    Dict,
    NamedTuple
)


# Types bridge
# Use this `types` to handle global standard type definition
# Add providers/transaction/ types based on network lib
# eg. BaseProvider for web3
Hash32 = NewType("Hash32", bytes)
HexStr = NewType("HexStr", str)
Primitives = Union[bytes, int, bool]
TxCall = NewType("TxCall", NamedTuple)
TxAnswer = NewType("TxAnswer", NamedTuple)

Hash = Union[HexBytes, Hash32, HexStr]
Address = Union[Hash, bytes, str]
Provider = Union[Type[BaseProvider], Any]
SignedTransaction = NewType("SignedTransaction", NamedTuple)

PrivateKey = Union[Address, str]
Directory = NewType("Directory", str)
Command = NewType("Commands", str)
Uri = NewType("URI", str)
Abi = NewType("Abi", Dict[Any, Any])
CIDStr = NewType("CIDStr", str)
Codec = Type[Formats]

# By convention var types should start with "T" followed by type name
TFunctions = TypeVar("TFunctions", covariant=True)
TEvents = TypeVar("TEvents", covariant=True)


class Subscriptable(Protocol):
    def __getattr__(self, name: str) -> Any:
        ...


