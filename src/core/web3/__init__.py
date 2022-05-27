"""
https://docs.python.org/3/library/typing.html#module-typing
Note: The Python runtime does not enforce function and variable type annotations.
They can be used by third party tools such as type checkers, IDEs, linters, etc.
"""

from enum import Enum
from abc import ABCMeta, abstractmethod
from typing import Any
from ..types import (
    Abi,
    Address,
    Provider,
    PrivateKey,
    Request,
    Transaction,
    Hash,
    SignedTransaction,
    Contract as _Contract,
)


class ChainID(Enum):
    Kovan = 42
    Rinkeby = 4


class NetworkID(Enum):
    Ethereum = 0

    def __str__(self) -> str:
        return self.name


class ContractID(Enum):
    ERC1155 = 1155
    ERC20 = 20

    def __str__(self) -> str:
        return self.name


class Chain(metaclass=ABCMeta):
    """Chain abstract class

    Hold/specify the artifacts/methods needed to interact with chain.
    Use this class to create chain subtypes.

    Usage:
        class Kovan(Chain):
            ....

    """

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    @abstractmethod
    def id(self) -> ChainID:
        """Return chain id

        eg. Kovan -> 42, Rinkeby -> 4
        :return: integer representation for chain
        :rtype: ChainID
        """
        pass

    @abstractmethod
    def connector(self) -> Provider:
        """Return the connector interface

        Provide a connector to interact with chain.
        eg. Http | Websocket
        """
        pass

    @property
    @abstractmethod
    def private_key(self) -> PrivateKey:
        """Return specific private key for chain

        :return: private key
        :rtype: HexAddress
        """
        pass

    @property
    @abstractmethod
    def erc1155(self) -> Address:
        """Return address for deployed contract

        :return: nft contract address
        :rtype: HexAddress
        """
        pass


class Network(metaclass=ABCMeta):
    """Network abstract class

    Specify all methods needed to interact with the blockchain.
    Use this class to create blockchain subtypes.

    Usage:
        class Algorand(Network):
            ....

    """

    chain: Chain

    def __init__(self, chain: Chain):
        """Assoc chain with network"""
        super().__init__()
        self.chain = chain

    @abstractmethod
    def set_default_account(self, account: Address) -> Address:
        """Set default account for blockchain operations

        :param account: The account to subscribe
        :return: account subscribed
        :rtype: Account
        """
        pass

    @abstractmethod
    def contract(self, address: Address, abi: Abi) -> _Contract:
        """Return contract for blockchain operations.
        This factory method return a prebuilt contract based on blockchain specifications.

        :param account: The account to subscribe
        :return: Account subscribed
        :rtype: Account
        """
        pass

    @abstractmethod
    def sign_transaction(self, tx: Request) -> SignedTransaction:
        """Sign transaction for blockchain using private key.

        :return: Signed transaction
        :rtype: eth_account.datastructures.SignedTransaction
        """
        pass

    @abstractmethod
    def send_transaction(self, tx: Request) -> Hash:
        """Commit signed transaction to blockchain.

        :return: Transaction hash
        :rtype: HexBytes
        """
        pass

    @abstractmethod
    def get_transaction(self, hash: Hash) -> Transaction:
        """Return transaction summary

        :param tx: transaction address
        :return: Transaction summary
        :rtype: Transaction
        """
        pass


class Contract(metaclass=ABCMeta):
    """Contract abstract class

    Specify all methods needed to interact with contracts.
    Use this class to create contract subtypes.

    Usage:
        class NFT(Contract):
            ....

    """

    address: Address
    functions: Any

    def __init__(self, network: Network):
        """Connect contract to network"""
        super().__init__()
        self.network = network

    @abstractmethod
    def __getattr__(self, name: str) -> Any:
        """Descriptor called when an attribute lookup has not found the attribute in the usual places"""
        pass

    @property
    @abstractmethod
    def abi(self) -> Abi:
        """Return contract abi for contract

        :param root_path: Where is abi.json stored?
        :return: abi json
        :rtype: dict
        """
        pass
