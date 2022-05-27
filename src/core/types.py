from hexbytes import HexBytes
from web3.contract import Contract as _Contract
from web3.providers.base import BaseProvider
from typing import NewType, Union, Any, Type
from eth_account.datastructures import SignedTransaction as _Signed
from eth_typing.evm import ChecksumAddress
from eth_typing.encoding import HexStr
from web3.types import TxParams, TxData
from ffmpeg_streaming import Formats


# Types bridge
# Use this `types` to handle global standard type definition
# Add providers/transaction/ types based on network lib
# eg. BaseProvider for web3
Primitives = Union[bytes, int, bool]
Request = Union[TxParams, Any]
Transaction = Union[TxData, Any]
Address = Union[ChecksumAddress, Any]
Provider = Union[Type[BaseProvider], Any]
Contract = Union[Type[_Contract], Any]
Hash = Union[HexBytes, HexStr]
SignedTransaction = Union[_Signed, Any]

PrivateKey = Union[Address, str]
Directory = NewType("Directory", str)
Abi = NewType("Abi", dict)
CIDStr = NewType("CIDStr", str)
Codec = Type[Formats]
