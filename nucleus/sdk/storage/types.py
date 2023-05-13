from dataclasses import dataclass
from nucleus.sdk.processing import File
from nucleus.core.types import (
    Protocol,
    CID,
    NewType,
    Optional,
    Union,
    URL,
    Callable,
    JSON,
    runtime_checkable,
)


@dataclass(slots=True)
class Object:
    """Distributed/Stored media representation.
    This class is used to infer any media decentralized and already stored in IPFS
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
ID = NewType("ID", str)
Storable = Union[File, JSON, str, bytes]
Store = Callable[[Storable], Object]


@runtime_checkable
class Service(Protocol):
    """Storage abstraction to manage the configuration needed to connect to services.
    Use this class to create Services subtypes.
    """

    def endpoint(self) -> URL:
        """Return the service endpoint

        return: the url endpoint
        :rtype: URL
        """
        ...

    def key(self) -> str:
        """Return the service authentication key

        :return: the key string
        :rtype: str
        """
        ...


class Edge(Protocol):
    """Edge provides an standard interface to handle ipfs storage services.
    For each storage service methods should be defined and encapsulate with any needed logic to simplify the usage.
    Use this class to create edge services subtypes.

    Each storage service represent a remote cache service like 'pinata', 'filebase' or any service that support remote pinning service.
    ref: https://docs.ipfs.tech/reference/kubo/cli/#ipfs-pin-remote-service
    """

    def pin(self, obj: Object) -> Pin:
        """Pin cid into remote storage

        :param obj: object to pin
        :return: pin object
        :rtype: Pin
        """
        ...

    def unpin(self, obj: Object) -> CID:
        """Remove pin from storage service

        :param obj: object to remove from service
        :return: just removed object cid
        :rtype: CID
        """
        ...


__all__ = ("Pin", "Service", "Storable", "Store", "Edge", "Object")
