from . import Transaction
from hexbytes import HexBytes
from dataclasses import dataclass


@dataclass
class EthereumTransaction(Transaction):
    blockHash: HexBytes
    blockNumber: int
    chainId: int
    gas: int
    gasPrice: int
    hash: HexBytes
    nonce: int
    to: str
    value: int
