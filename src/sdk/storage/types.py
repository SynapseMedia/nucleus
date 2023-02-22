from abc import ABCMeta, abstractmethod
from src.core.types import Sequence, Protocol
from src.core.ipfs.types import Service, RemotePin


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

    @property
    @abstractmethod
    def name(self) -> str:
        """Return service name from name attribute in Service"""
        ...

    @abstractmethod
    def pin(self, cid: str) -> RemotePin:
        """Pin cid in remote edge cache
        ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-add

        :param cid: cid to pin
        :return: RemotePin object
        :rtype: RemotePin
        """
        ...

    @property
    @abstractmethod
    def background_mode(self) -> bool:
        """Pin cid in async mode
        ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-add

        :return: True if running in async mode else False
        :rtype: bool
        """
        ...

    @property
    @abstractmethod
    def is_registered(self) -> bool:
        """Check if service is registered

        :return: True if service is registered else False
        :rtype: bool
        """
        ...

    @property
    @abstractmethod
    def status(self) -> bool:
        """Check status for edge service

        :return: True if auth ready and registered else False
        :rtype: bool
        """
        ...

    @abstractmethod
    def ls(self, limit: int) -> Sequence[RemotePin]:
        """Return current remote pin list
        ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-ls

        :param limit: Number of remote pins to return
        :return: List of current remote pin list
        :rtype: Sequence[RemotePin]
        """
        ...

    @abstractmethod
    def unpin(self, cid: str) -> bool:
        """Remove pin from edge cache service

        :param cid: Cid to remove from cache
        :return: True if pin was removed else False
        :rtype: bool
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
