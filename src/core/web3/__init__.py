"""
https://docs.python.org/3/library/typing.html#module-typing
Note: The Python runtime does not enforce function and variable type annotations.
They can be used by third party tools such as type checkers, IDEs, linters, etc.
"""

from enum import Enum
from web3 import types
from dataclasses import dataclass
from abc import ABC, abstractmethod
from eth_account import Account


class ChainID(Enum):
    Kovan = 42
    Rinkeby = 4


class NetworkID(Enum):
    Ethereum = 0

    def __str__(self):
        return self.name


class ContractID(Enum):
    ERC1155 = 1155
    ERC20 = 20

    def __str__(self):
        return self.name


@dataclass
class Transaction:
    pass


class Chain(ABC):
    """Chain abstract class

    Hold/specify the artifacts/methods needed to interact with chain.
    Use this class to create chain subtypes.

    Usage:
        class Kovan(Chain):
            ....

    """

    @abstractmethod
    def __str__(self):
        pass

    @property
    @abstractmethod
    def id():
        """Return chain id

        eg. Kovan -> 42, Rinkeby -> 4
        :return: integer representation for chain
        :rtype: int
        """
        pass

    @abstractmethod
    def connector(self):
        """Return the connector interface

        Provide a connector to interact with chain.
        eg. Http | Websocket
        """
        pass

    @property
    @abstractmethod
    def private_key(self):
        """Return specific private key for chain

        :return: private key
        :rtype: str
        """
        pass

    @property
    @abstractmethod
    def erc1155(self):
        """Return address for deployed contract

        :return: nft contract address
        :rtype: str
        """
        pass


class Network(ABC):
    """Network abstract class

    Specify all methods needed to interact with the blockchain.
    Use this class to create blockchain subtypes.

    Usage:
        class Algorand(Network):
            ....

    """

    def __init__(self, chain: Chain):
        """Assoc chain with network

        :param chain: chain to connect. eg. Rinkeby, Kovan, etc..
        :return: chain connected
        :rtype: Chain
        """

        super().__init__()
        self.chain = chain

    @abstractmethod
    def set_default_account(self, account: Account):
        """Set default account for blockchain operations

        :param account: The account to subscribe
        :return: account subscribed
        :rtype: Account
        """
        pass

    @abstractmethod
    def contract(self, address: str, abi: str):
        """Return contract for blockchain operations.
        This factory method return a prebuilt contract based on blockchain specifications.

        :param account: The account to subscribe
        :return: Account subscribed
        :rtype: Account
        """
        pass

    @abstractmethod
    def sign_transaction(self, tx):
        """Sign transaction for blockchain using private key.

        :return: Signed transaction
        :rtype: eth_account.datastructures.SignedTransaction
        """
        pass

    @abstractmethod
    def send_transaction(self):
        """Commit signed transaction to blockchain.

        :return: Transaction hash
        :rtype: HexBytes
        """
        pass

    @abstractmethod
    def get_transaction(hash: types._Hash32):
        """Return transaction summary

        :param tx: transaction address
        :return: Transaction summary
        :rtype: TxData
        """
        pass


class Contract(ABC):
    """Contract abstract class

    Specify all methods needed to interact with contracts.
    Use this class to create contract subtypes.

    Usage:
        class NFT(Contract):
            ....

    """

    def __init__(self, network: Network):

        """Connect contract to network

        :param network: Network to connect within
        :return: network connected
        :rtype: Network
        """
        super().__init__()
        self.network = network

    def __getattr__(self, name: str):
        """Called when an attribute lookup has not found the attribute in the usual places"""
        pass

    @property
    @abstractmethod
    def abi(root_path: str):
        """Return contract abi for contract

        :param root_path: Where is abi.json stored?
        :return: abi json
        :rtype: dict
        """
        pass
