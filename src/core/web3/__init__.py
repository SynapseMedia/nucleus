"""
https://docs.python.org/3/library/typing.html#module-typing
Note: The Python runtime does not enforce function and variable type annotations.
They can be used by third party tools such as type checkers, IDEs, linters, etc.
"""

from enum import Enum
from abc import ABCMeta, abstractmethod
from typing import Any, Generic
from ..types import (
    Abi,
    Address,
    Provider,
    PrivateKey,
    TxCall,
    TxAnswer,
    Hash,
    SignedTransaction,
    Contract as _Contract,
    TFunctions,
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


class ProxyContract(Generic[TFunctions]):
    """This class pretends to handle generically the function calls to contract

    eg.
        # Contract can be any based on lib
        # Every network lib expose in a different way the programmatic call to functions

        # using Web3
        c = Contract()
        c.functions.mint() <- how can we handle `mint` for any different lib?

        probably we need an standard interface here?

        c = Contract()
        c.mint() # Does'nt matter how the call is made underneath

    usage:

        ProxyContract[TFunctions, TEvents..](Contract)

    """

    interface: _Contract[TFunctions]  # Subscriptable object needed
    functions: TFunctions

    def __init__(self, interface: _Contract[TFunctions]):
        self.interface = interface
        self.functions = interface.functions

    def __getattr__(self, name: str):
        """Proxy call to subscriptable interface"""
        if not hasattr(self.interface, name):
            # By default answer with function calls
            return getattr(self.functions, name)
        return getattr(self.interface, name)


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
    def set_default_account(self, account: Address) -> None:
        """Set default account for network operations"""
        ...

    @abstractmethod
    def build_contract(self, address: Address, abi: Abi) -> ProxyContract[Any]:
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


class Contract(metaclass=ABCMeta):
    """Contract abstract class

    Specify all methods needed to interact with contracts.
    Use this class to create contract subtypes.

    Usage:
        class NFT(Contract):
            ....

    """

    address: Address
    _proxy: ProxyContract[Any]

    def __init__(self, network: Network):
        """Connect contract to network"""
        super().__init__()
        self.network = network

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
