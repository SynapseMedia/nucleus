"""
Note: The Python runtime does not enforce function and variable type annotations.
They can be used by third party tools such as type checkers, IDEs, linters, etc.

refs:
- https://docs.python.org/3/library/typing.html#module-typing
- https://peps.python.org/pep-0544/#protocol-members
- https://google.github.io/pytype/errors.html#bad-return-type
"""

from enum import Enum
from abc import ABCMeta, abstractmethod
from typing import Any, Protocol, Union, NewType, TypedDict, NamedTuple, Dict, Callable
from ..types import Subscriptable, Endpoint, HexStr, Hash

Address = Union[HexStr, str]
Abi = NewType("Abi", Dict[Any, Any])
Connector = Callable[[Endpoint], Any]
PrivateKey = Union[Address, int]
TxCall = Union[NamedTuple, TypedDict]
TxAnswer = Union[NamedTuple, TypedDict]
SignedTransaction = NewType("SignedTransaction", NamedTuple)


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


class Provider(Protocol, metaclass=ABCMeta):
    """This protocol enforce adapter usage for Lib connectors and Chains

    We don't know how each lib handle their connection to providers or endpoints for each networks
        - for web3 lib we have HTTP, ICP, Websocket
        - for algorand we can use AlgoClient to connect a node

    This probably cause an issue for standard usage, if we use an adapter we can wrap an existing
    class with a new interface that we know.

    Usage:
        class Web3HTTPProviderAdapter(Provider):
            def __call__(self):
                ...any logic here
                def __connect(endpoint: Endpoint):
                    return HTTPProvider(endpoint)
                return __connect


        class AlgorandProviderAdapter(Provider):
            def __call__(self):
                ...any logic here
                def __connect(endpoint: Endpoint):
                    return algod.AlgodClient(endpoint)
                return __connect


        class AnyOtherProviderAdapter(Provider):
            def __call__(self):
                def __connect(endpoint: Endpoint):
                    # Build here the connector logic
                return __connect
    """

    @abstractmethod
    def __call__(cls) -> Connector:
        """Call take build/setup the connector and return a callable or function

        This method will ensure that always we get the same interface for use in each corresponding network

        :return: Connector is a callable Callable[Endpoint, ExpectedConnector]
        :rtype: Connector
        """
        ...


class Proxy(Subscriptable, metaclass=ABCMeta):
    """This protocol pretends to enforce generically calls to unknown methods

    eg.
        # Contract can be any based on lib
        # Every network lib expose in a different way the programmatic call to functions

        # using Web3
        c = Contract()

        # We don't know the accessor for functions for every lib
        c.functions.mint() <- how can we handle `mint` for any different lib?

        # So...
        # probably we need an standard interface here to delegate calls?

        c = Contract()
        c.mint() # Does'nt matter how the call is made underneath

    """

    @abstractmethod
    def __init__(self, interface: Any):
        """Interface may be anything but MUST expose a subscriptable object to handle it"""
        ...

    @abstractmethod
    def __getattr__(self, name: str) -> Subscriptable:
        """Control behavior for when a user attempts to access an attribute that doesn't exist

        This method proxies/delegate the call to low level lib subscriptable object

        # Example with web3 lib
        class Web3Functions:
            def __getattr__(self, name):
                # Here the low level lib handle the function call to contract

        # Underneath core lib web3
        class Web3Contract:
            functions = Web3Functions <- this is now an subscriptable object

        # Our proxy is an subscriptable object too
        contract = CustomContract(Proxy)

        # In a transitive approach we delegate the call to our `favorite lib` using our "CustomContract"
        contract.[myMethod]() <- this is not an existing method in our contract so we delegate the call to our lib contract functions

        Usage:
            class ProxyWeb3Contract(Proxy):
                interface: Contract

                def __init__(self, interface: Contract):
                    self.interface = interface

                def __getattr__(self, name: str):
                    return getattr(self.interface.functions, name)

        :return: default subscriptable object
        :rtype: Subscriptable

        """
        ...


class Chain(Protocol, metaclass=ABCMeta):
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

    @property
    @abstractmethod
    def endpoint(self) -> Endpoint:
        """Return connection string to provider

        :return: Endpoint to connect with provider
        :rtype: Endpoint
        """
        ...

    @property
    @abstractmethod
    def provider(self) -> Provider:
        """Return the connector adapter interface

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


class Network(Protocol, metaclass=ABCMeta):
    """Network abstract class

    Specify all methods needed to interact with the blockchain.
    Use this class to create blockchain subtypes.

    Usage:
        class Algorand(Network):
            ....

    """

    _chain: Chain

    @abstractmethod
    def __init__(self, chain: Chain):
        """Assoc chain with network"""
        ...

    @property
    @abstractmethod
    def chain(self) -> Chain:
        ...

    @abstractmethod
    def set_default_account(self, private_key: PrivateKey) -> None:
        """Set default account for network operations

        :param private_key: wallet key address
        :raises InvalidPrivateKey
        """
        ...

    @abstractmethod
    def contract(self, address: Address, abi: Abi) -> Proxy:
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


class Contract(Protocol, metaclass=ABCMeta):
    """Contract abstract class

    Specify all methods needed to interact with contracts.
    Use this class to create contract subtypes.

    Usage:
        class NFT(Contract):
            ....

    """

    _address: Address
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
