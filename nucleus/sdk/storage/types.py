from dataclasses import dataclass

from nucleus.core.types import (
    CID,
    JSON,
    Callable,
    NewType,
    Optional,
    Protocol,
    Union,
)
from nucleus.sdk.processing import File


@dataclass(slots=True)
class Object:
    """Distributed/Stored media representation.
    This class is used to represent any media decentralized and already stored in IPFS.

    Usage:

        # generally, these objects are returned by storage operations
        stored_object = Object("bafyjvzacdjrk37kqvy5hbqepmcraz3txt3igs7dbjwwhlfm3433a","image",250)
    """

    hash: CID
    name: str
    size: int


@dataclass(slots=True)
class Pin:
    """Represents ipfs /pin output

    Usage:

        # generally, these objects are returned by pin operations
        stored_object = Object("bafyjvzacdjrk37kqvy5hbqepmcraz3txt3igs7dbjwwhlfm3433a","pinned", "image.jpg")
    """

    cid: CID
    status: str
    name: Optional[str]


# Alias for allowed media to store
ID = NewType('ID', str)
Storable = Union[File, JSON, str, bytes]
Store = Callable[[Storable], Object]


class Client(Protocol):
    """Provides an standard interface for handling IPFS storage services. Each storage service
    represents a remote cache service, such as Estuary. This class can be used as a base to
    create subtypes for specific edge clients.

    Usage:

        # our own service implementation
        class EdgeService:

            def pin(self, obj: Object, **kwargs: Any) -> Pin:
                # Implementation for pinning the object
                ...

            def unpin(self, cid: CID) -> CID:
                # Implementation for unpinning the CID
                ...

    """

    def pin(self, obj: Object) -> Pin:
        """Pin cid to storage service

        :param obj: Object to pin
        :return: Pin object
        """
        ...

    def unpin(self, cid: CID) -> CID:
        """Remove pin from storage service

        :param cid: The cid to remove from service
        :return: The just removed object cid
        """
        ...


__all__ = ('Pin', 'Storable', 'Store', 'Client', 'Object')
