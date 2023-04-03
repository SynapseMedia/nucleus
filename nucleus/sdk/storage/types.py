from dataclasses import dataclass
from nucleus.sdk.harvest.models import Media, Meta
from nucleus.core.types import Protocol, Path, CID, NewType, Optional, Union, JSON


# Alias for allowed media to store
Storable = Union[Media[Path], Meta]
ID = NewType("ID", str)


@dataclass
class Stored:
    """Represents ipfs /add output"""

    cid: CID
    name: str
    size: float


@dataclass
class Pin:
    """Represents ipfs /pin output"""

    cid: CID
    status: str
    name: Optional[str]


class Edge(Protocol):
    """Edge provides an standard interface to handle ipfs edge services.
    For each edge service methods should be defined and encapsulate with any needed logic to simplify the usage.
    Use this class to create edge services subtypes.

    Each edge service represent a remote cache service like 'pinata', 'filebase' or any service that support remote pinning service.
    ref: https://docs.ipfs.tech/reference/kubo/cli/#ipfs-pin-remote-service
    """

    def pin(self, cid: CID) -> JSON:
        """Pin cid into remote edge cache

        :param cid: cid to pin
        :return: service response as json
        :rtype: JSON
        """
        ...

    def unpin(self, cid: CID):
        """Remove pin from edge cache service

        :param cid: Cid to remove from cache
        :return: none
        :rtype: None
        """
        ...
