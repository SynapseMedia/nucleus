from enum import Enum
from abc import ABCMeta, abstractmethod
from src.core.types import (
    URL,
    HexStr,
    Any,
    Protocol,
    Union,
    NewType,
    TypedDict,
    NamedTuple,
    Callable,
    JSON,
)

Address = Union[HexStr, str]
Abi = NewType("Abi", JSON)
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
    def private_key(self) -> PrivateKey:
        """Return specific private key for chain

        :return: private key
        :rtype: PrivateKey
        """
        ...


# TODO refactor segregate interfaces
class Network(Protocol, metaclass=ABCMeta):
    """Network abstract class.

    Bridge all methods needed to interact with networks.
    Use this class to create networks subtypes.

    Usage:
        class Algorand(Network):
            ....

    """

    @abstractmethod
    def __init__(self, chain: Chain):
        """Assoc chain with network"""
        ...


# TODO refactor
class Contract(Protocol, metaclass=ABCMeta):
    """Contract abstract class

    Bridge all methods needed to interact with contracts.
    Use this class to create contract subtypes.

    Usage:
        class NFT(Contract):
            ....

    """

    @abstractmethod
    def __init__(self, network: Network):
        """Connect contract to network"""
        ...
