from . import TxRequest
from hexbytes import HexBytes
from dataclasses import dataclass


@dataclass
class EthereumTransaction(TxRequest):
    blockHash: HexBytes
    blockNumber: int
    chainId: int
    gas: int
    gasPrice: int
    hash: HexBytes
    nonce: int
    to: str
    value: int

    def __hash__(self):
        return self.blockHash