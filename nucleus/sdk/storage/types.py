from dataclasses import dataclass

from nucleus.core.types import (
    CID,
    JSON,
    URL,
    Callable,
    NewType,
    Optional,
    Protocol,
    Union,
    runtime_checkable,
)
from nucleus.sdk.processing import File


@dataclass(slots=True)
class Object:
    """Distributed/Stored media representation.
    This class is used to represent any media decentralized and already stored in IPFS.
    """

    hash: CID
    name: str
    size: int


@dataclass(slots=True)
class Pin:
    """Represents ipfs /pin output"""

    cid: CID
    status: str
    name: Optional[str]


# Alias for allowed media to store
ID = NewType('ID', str)
Storable = Union[File, JSON, str, bytes]
Store = Callable[[Storable], Object]


@runtime_checkable
class Service(Protocol):
    """specifies the methods required to establish connections with services.
    This class can be used as a base to create subtypes for different services.
    """

    def endpoint(self) -> URL:
        """Return the service endpoint

        return: the url endpoint
        """
        ...

    def key(self) -> str:
        """Return the service authentication key

        :return: the key string
        """
        ...


class Client(Protocol):
    """provides a standardized interface for handling IPFS storage services. Each storage service
    represents a remote cache service, such as Estuary. This class can be used as a base to 
    create subtypes for specific edge clients.
    """

    def pin(self, obj: Object) -> Pin:
        """Pin cid into remote storage

        :param obj: Object to pin
        :return: Pin object
        """
        ...

    def unpin(self, obj: Object) -> CID:
        """Remove pin from storage service

        :param obj: Object to remove from service
        :return: Just removed object cid
        """
        ...


__all__ = ('Pin', 'Service', 'Storable', 'Store', 'Client', 'Object')
