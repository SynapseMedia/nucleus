from hexbytes import HexBytes
from web3.providers.base import BaseProvider
from typing import NewType, Union, Any, Type, TypedDict, TypeVar, Protocol
from eth_account.datastructures import SignedTransaction as _Signed
from eth_typing.evm import ChecksumAddress
from eth_typing.encoding import HexStr
from web3.types import TxParams, TxData
from ffmpeg_streaming import Formats  # type: ignore


# Types bridge
# Use this `types` to handle global standard type definition
# Add providers/transaction/ types based on network lib
# eg. BaseProvider for web3
Primitives = Union[bytes, int, bool]
TxRequest = Union[TxParams, TypedDict]
Transaction = Union[TxData, TypedDict]
Address = Union[ChecksumAddress, Any]
Provider = Union[Type[BaseProvider], Any]
SignedTransaction = Union[_Signed, Any]
Hash = Union[HexBytes, HexStr]

PrivateKey = Union[Address, str]
Directory = NewType("Directory", str)
Command = NewType("Commands", str)
Uri = NewType("URI", str)
Abi = NewType("Abi", dict)
CIDStr = NewType("CIDStr", str)
Codec = Type[Formats]

TFunctions = TypeVar("TFunctions", covariant=True)
TEvents = TypeVar("TEvents", covariant=True)

class Contract(Protocol[TFunctions]):
    @property
    def functions(self) -> TFunctions:
        ...
