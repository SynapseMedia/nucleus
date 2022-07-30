from abc import ABCMeta, abstractmethod
from src.core.types import (
    Sequence,
    TypedDict,
    Any,
    Optional,
    Mapping,
    Iterator,
    Protocol,
    Tuple,
    Endpoint,
)


class Service(TypedDict):
    service: str
    endpoint: Endpoint
    key: Optional[str]


class DagLink(TypedDict):
    name: Optional[str]
    hash: Mapping[str, str]
    tsize: int


class Dag(TypedDict):
    data: Mapping[str, Mapping[str, str]]
    links: Iterator[DagLink]


# Exec type contains standardize output for ipfs commands.
# An issue here is that ipfs returns different encodings for each command, sometimes could be a string and later probably we get a json object,
# so using "output" could be fine to expect always the same field to process.
# eg. output = exec.get("output")
# ref: docs.ipfs.io/reference/cli/#ipfs
Exec = TypedDict("Exec", {"output": Any})
Services = TypedDict("Services", {"remote": Iterator[Service]})

# Pin types
LocalPin = TypedDict("Pin", {"pins": Sequence[str]})


class RemotePin(TypedDict):
    cid: str
    status: str
    name: str


class Container(Protocol, metaclass=ABCMeta):
    """
    Docker container abstraction adapted from docker lib
    """

    @abstractmethod
    def exec_run(self, cmd: str) -> Tuple[bool, bytes]:
        ...


# Available edge services supported
class Edge(Protocol, metaclass=ABCMeta):
    _service: Service

    @abstractmethod
    def __init__(self, service: Service):
        ...

    @property
    @abstractmethod
    def name(self) -> str:
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
