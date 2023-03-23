from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from nucleus.sdk.harvest.model import Media
from nucleus.core.types import (
    Iterator,
    Protocol,
    Path,
    CID,
    NewType,
    Optional,
)

# Alias for allowed media to store
Storable = Media[Path]
ID = NewType("ID", str)


@dataclass
class Pin:
    cid: CID
    status: str
    name: Optional[str]


class Edge(Protocol, metaclass=ABCMeta):
    """Edge provides an standard facade interface to handle services in IPFS.
    For each edge service methods should be defined and encapsulate with any needed logic to simplify the usage.
    Use this class to create edge services subtypes.

    Each edge service represent a remote cache service like 'pinata', 'filebase' or any service that support remote pinning service.
    ref: https://docs.ipfs.tech/reference/kubo/cli/#ipfs-pin-remote-service
    """

    @abstractmethod
    def pin(self, cid: CID) -> Pin:
        """Pin cid into remote edge cache

        :param cid: cid to pin
        :return: pin object
        :rtype: Pin
        """
        ...

    @abstractmethod
    def ls(self) -> Iterator[Pin]:
        """Return current remote pin list

        :param limit: number of remote pins to return
        :return: list of current remote pin list
        :rtype: Iterator[Pin]
        """
        ...

    @abstractmethod
    def unpin(self, cid: CID):
        """Remove pin from edge cache service

        :param cid: Cid to remove from cache
        :return: none
        :rtype: None
        """
        ...
