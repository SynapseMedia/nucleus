"""
Note: The Python runtime does not enforce function and variable type annotations.
They can be used by third party tools such as type checkers, IDEs, linters, etc.

refs:
- https://docs.python.org/3/library/typing.html#module-typing
- https://peps.python.org/pep-0544/#protocol-members
"""

from enum import Enum
from abc import abstractmethod
from typing import Any, Protocol
from ..types import (
    Abi,
    Address,
    Provider,
    PrivateKey,
    TxCall,
    TxAnswer,
    Hash,
    SignedTransaction,
    Subscriptable,
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


class Proxy(Protocol):
    """This protocol pretends to enforce generically calls to unknown methods

    eg.
        # Contract can be any based on lib
        # Every network lib expose in a different way the programmatic call to functions

        # using Web3
        c = Contract()

        # We don't know the accessor for functions for every lib
        c.functions.mint() <- how can we handle `mint` for any different lib?

        # So...
        # probably we need an standard interface here?

        c = Contract()
        c.mint() # Does'nt matter how the call is made underneath

    """

    @abstractmethod
    def __init__(self, interface: Any):
        ...

    @abstractmethod
    def __getattr__(self, name: str) -> Subscriptable:
        """Proxy call to subscriptable interface"""
        ...


class Chain(Protocol):
    """Chain abstract class

    Hold/specify the artifacts/methods needed to interact with chain.
    Use this class to create chain subtypes.

    Usage:
        class Kovan(Chain):
            ....

    """

    @abstractmethod
    def __str__(self) -> str:
        ...

    @property
    @abstractmethod
    def id(self) -> ChainID:
        """Return chain id

        eg. Kovan -> 42, Rinkeby -> 4
        :return: integer representation for chain
        :rtype: ChainID
        """
        ...

    @abstractmethod
    def connector(self) -> Provider:
        """Return the connector interface

        Provide a connector to interact with chain.
        eg. Http | Websocket
        :return: Provider interface to bind network
        :rtype: Provider
        """
        ...

    @property
    @abstractmethod
    def private_key(self) -> PrivateKey:
        """Return specific private key for chain

        :return: private key
        :rtype: PrivateKey
        """
        ...

    @property
    @abstractmethod
    def erc1155(self) -> Address:
        """Return address for deployed contract

        :return: nft contract address
        :rtype: Address
        """
        ...


class Network(Protocol):
    """Network abstract class

    Specify all methods needed to interact with the blockchain.
    Use this class to create blockchain subtypes.

    Usage:
        class Algorand(Network):
            ....

    """

    chain: Chain

    @abstractmethod
    def __init__(self, chain: Chain):
        """Assoc chain with network"""
        ...

    @abstractmethod
    def set_default_account(self, private_key: PrivateKey) -> None:
        """Set default account for network operations

        :param private_key: wallet key address
        :raises InvalidPrivateKey
        """
        ...

    @abstractmethod
    def contract_factory(self, address: Address, abi: Abi) -> Proxy:
        """Return contract for blockchain operations.
        This factory method return a prebuilt contract based on blockchain specifications.

        :param address: Contract address
        :param abi: Abi dict source
        :return: Contract interface
        :rtype: Contract
        """
        ...

    @abstractmethod
    def sign_transaction(self, tx: TxCall) -> SignedTransaction:
        """Sign transaction for blockchain using private key.

        :return: Signed transaction
        :rtype: SignedTransaction
        """
        ...

    @abstractmethod
    def send_transaction(self, tx: TxCall) -> Hash:
        """Commit signed transaction to blockchain.

        :return: Transaction hash
        :rtype: Hash
        """
        ...

    @abstractmethod
    def get_transaction(self, hash: Hash) -> TxAnswer:
        """Return transaction summary

        :param tx: transaction address
        :return: Transaction summary
        :rtype: Transaction
        """
        ...


class Contract(Protocol):
    """Contract abstract class

    Specify all methods needed to interact with contracts.
    Use this class to create contract subtypes.

    Usage:
        class NFT(Contract):
            ....

    """

    address: Address
    network: Network
    _proxy: Proxy

    @abstractmethod
    def __init__(self, network: Network):
        """Connect contract to network"""
        ...

    @abstractmethod
    def __getattr__(self, name: str) -> Any:
        """Descriptor called when an attribute lookup has not found the attribute in the usual places"""
        ...

    @property
    @abstractmethod
    def abi(self) -> Abi:
        """Return contract abi for contract

        :param root_path: Where is abi.json stored?
        :return: abi json
        :rtype: Abi
        """
        ...
