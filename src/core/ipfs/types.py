from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from src.core.types import (
    Sequence,
    Optional,
    Mapping,
    Iterator,
    Protocol,
    Tuple,
    URL,
    NewType,
    CID,
)

ID = NewType("ID", str)


@dataclass
class Service:
    name: str = ""  # Service name. eg. estuary, pinata, filebase.
    endpoint: URL = URL("")  # api endpoint provided by service.
    key: Optional[str] = None  # auth key provided by service


@dataclass
class DagLink:
    name: Optional[str]
    hash: Mapping[str, str]
    tsize: int


@dataclass
class Dag:
    data: Mapping[str, Mapping[str, str]]
    links: Iterator[DagLink]


@dataclass
class Pin:
    cid: CID
    status: str
    name: Optional[str]


@dataclass
class Services:
    remote: Iterator[Service]


@dataclass
class LocalPin:
    pins: Sequence[str]


class Container(Protocol, metaclass=ABCMeta):
    """Docker container abstraction adapted from docker lib"""

    @abstractmethod
    def exec_run(self, cmd: str) -> Tuple[bool, bytes]:
        ...
