from abc import ABCMeta, abstractmethod
from nucleus.core.types import (
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


class Chain(Protocol, metaclass=ABCMeta):
    """Chain abstract class.
    Use this class to create chain subtypes.

    Usage:
        class Kovan(Chain):
            ....

    """

    @abstractmethod
    def __str__(self) -> str:
        ...


class Network(Protocol, metaclass=ABCMeta):
    """Network bridge abstract class.
    Use this class to create networks subtypes.

    Usage:
        class Algorand(Network):
            ....

    """

    @abstractmethod
    def __init__(self, chain: Chain):
        """Assoc chain with network"""
        ...


class Contract(Protocol, metaclass=ABCMeta):
    """Contract abstract class
    Use this class to create contract subtypes.

    Usage:
        class NFT(Contract):
            ....

    """

    @abstractmethod
    def __init__(self, network: Network):
        """Connect contract to network"""
        ...
