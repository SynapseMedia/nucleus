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

    @abstractmethod
    def flush(self, limit: int) -> int:
        """Remove all pinned cid from edge cache service

        :param limit: maximum number of remote pins to remove
        :return: number of remote pins removed
        :rtype: int
        :raises EdgePinException: if an error occurs during request
        """
        ...
