from nucleus.core.types import (
    JSON,
    URL,
    Any,
    Callable,
    HexStr,
    NamedTuple,
    NewType,
    Protocol,
    TypedDict,
    Union,
)

Address = Union[HexStr, str]
Abi = NewType('Abi', JSON)
Connector = Callable[[URL], Any]
PrivateKey = Union[Address, int]
TxCall = Union[NamedTuple, TypedDict]
TxAnswer = Union[NamedTuple, TypedDict]
SignedTransaction = NewType('SignedTransaction', NamedTuple)


class Chain(Protocol):
    """Chain abstract class.
    Use this class to create chain subtypes.

    Usage:
        class Kovan(Chain):
            ....

    """

    def __str__(self) -> str:
        ...


class Network(Protocol):
    """Network bridge abstract class.
    Use this class to create networks subtypes.

    Usage:
        class Algorand(Network):
            ....

    """

    def __init__(self, chain: Chain):
        """Assoc chain with network"""
        ...


class Contract(Protocol):
    """Contract abstract class
    Use this class to create contract subtypes.

    Usage:
        class NFT(Contract):
            ....

    """

    def __init__(self, network: Network):
        """Connect contract to network"""
        ...
