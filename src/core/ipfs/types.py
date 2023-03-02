from abc import ABCMeta, abstractmethod
from src.core.types import (
    Sequence,
    Any,
    Optional,
    Mapping,
    Iterator,
    Protocol,
    Tuple,
    URL,
    NamedTuple,
    NewType,
    CID,
)


class Service(NamedTuple):
    name: str  # Service name. eg. pinata, filebase.
    endpoint: URL  # api endpoint provided by service
    key: Optional[str]  # auth key provided by service


class DagLink(NamedTuple):
    name: Optional[str]
    hash: Mapping[str, str]
    tsize: int


class Dag(NamedTuple):
    data: Mapping[str, Mapping[str, str]]
    links: Iterator[DagLink]


class Pin(NamedTuple):
    cid: CID
    status: str
    name: Optional[str]


# Result type contains standardize output for ipfs commands.
# An issue here is that ipfs returns different encodings for each command, sometimes could be a string and later probably we get a json object,
# so using "output" could be fine to expect always the same field to process.
# eg. call.output
# ref: docs.ipfs.io/reference/cli/#ipfs
ID = NewType("ID", str)
Result = NamedTuple("Result", output=Any)
Services = NamedTuple("Services", remote=Iterator[Service])
LocalPin = NamedTuple("Pin", pins=Sequence[str])


class Container(Protocol, metaclass=ABCMeta):
    """Docker container abstraction adapted from docker lib"""

    @abstractmethod
    def exec_run(self, cmd: str) -> Tuple[bool, bytes]:
        ...
