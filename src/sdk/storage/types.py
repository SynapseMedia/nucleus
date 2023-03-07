import requests
from abc import ABCMeta, abstractmethod
from src.core.types import Iterator, Protocol, Path, CID, JSON
from src.core.ipfs.types import Service, Pin
from src.sdk.harvest.model import Media

Headers = JSON
# Alias for allowed media to store
Storable = Media[Path]
# The Session object allows you to persist certain parameters across requests.
# It also persists cookies across all requests made from the Session instance.
Session = requests.Session
Response = requests.Response


class Edge(Protocol, metaclass=ABCMeta):
    """Edge provides an standard facade interface to handle services in IPFS.
    For each edge service methods should be defined and encapsulate with any needed logic to simplify the usage.

    Each edge service represent a remote cache service like 'pinata', 'filebase' or any service that support remote pinning service.
    ref: https://docs.ipfs.tech/reference/kubo/cli/#ipfs-pin-remote-service
    """

    _service: Service

    @abstractmethod
    def __init__(self, service: Service):
        ...

    @abstractmethod
    def pin(self, cid: CID) -> Pin:
        """Pin cid in remote edge cache
        ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-add

        :param cid: cid to pin
        :return: Pin object
        :rtype: Pin
        """
        ...

    @abstractmethod
    def ls(self) -> Iterator[Pin]:
        """Return current remote pin list
        ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-ls

        :return: list of current remote pin list
        :rtype: Iterator[Pin]
        """
        ...

    @abstractmethod
    def unpin(self, cid: CID):
        """Remove pin from edge cache service

        :param cid: Cid to remove from cache
        """
        ...

    @abstractmethod
    def flush(self, limit: int) -> int:
        """Remove all pinned cid from edge cache service

        :param limit: Maximum number of remote pins to remove
        :return: Number of remote pins removed
        :rtype: int
        """
        ...
