from enum import Enum
from abc import ABCMeta, abstractmethod
from src.core.types import (
    URL,
    HexStr,
    Hash,
    Any,
    Protocol,
    Union,
    NewType,
    TypedDict,
    NamedTuple,
    Callable,
    Raw,
    Proxy,
)

Address = Union[HexStr, str]
Abi = NewType("Abi", Raw)
Connector = Callable[[URL], Any]
PrivateKey = Union[Address, int]
TxCall = Union[NamedTuple, TypedDict]
TxAnswer = Union[NamedTuple, TypedDict]
SignedTransaction = NewType("SignedTransaction", NamedTuple)


class ChainID(Enum):
    Kovan = 42
    Rinkeby = 4
    Goerli = 6


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
    """Adapter protocol to enforce usage of Lib connectors

    We don't know how each lib handle their connection to providers or endpoints for each networks
        - for web3 lib we have HTTP, ICP, Websocket
        - for algorand we can use AlgoClient to connect a node

    This probably cause an issue for standard usage, if we use an adapter we can wrap an existing
    class with a new standard interface that we know.

    Usage:
        class Web3HTTPProviderAdapter(Provider):
            def __call__(self):
                ...any logic here
                def connect(endpoint: URL):
                    return HTTPProvider(endpoint)
                return connect


        class AlgorandProviderAdapter(Provider):
            def __call__(self):
                ...any logic here
                def connect(endpoint: URL):
                    return algod.AlgodClient(endpoint)
                return connect


        class AnyOtherProviderAdapter(Provider):
            def __call__(self):
                def connect(endpoint: URL):
                    # Build here the connector logic
                return connect
    """

    @abstractmethod
    def __call__(cls) -> Connector:
        """Call take build/setup the connector and return a callable or function

        This method will ensure that always we get the same interface for use in each corresponding network

        :return: Connector is a callable Callable[URL, ExpectedConnector]
        :rtype: Connector
        """
        ...


class Chain(Protocol, metaclass=ABCMeta):
    """Chain abstract class.

    Adapt the artifacts/methods needed to interact with chain.
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
    def endpoint(self) -> URL:
        """Return connection string to provider

        :return: URL to connect with provider
        :rtype: URL
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
    """Network abstract class.

    Bridge all methods needed to interact with networks.
    Use this class to create networks subtypes.

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
        :raises InvalidPrivateKey: if invalid key is provided
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

    Bridge all methods needed to interact with contracts.
    Use this class to create contract subtypes.

    Usage:
        class NFT(Contract):
            ....

    """

    _proxy: Proxy

    @abstractmethod
    def __init__(self, network: Network):
        """Connect contract to network"""
        ...

    @abstractmethod
    def __getattr__(self, name: str) -> Any:
        """Descriptor called when an attribute lookup has not found the attribute in the usual places
        Its intended to use for dynamically invoke function in contracts.
        """
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
