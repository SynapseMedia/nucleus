from abc import ABCMeta, abstractmethod
from src.core.types import (
    Sequence,
    TypedDict,
    Any,
    Optional,
    Mapping,
    Literal,
    Iterator,
    Protocol,
    Tuple
)


class EdgeService(TypedDict, total=False):
    service: str
    endpoint: str
    key: Optional[str]


class Edge(TypedDict):
    cid: str
    status: str
    name: str


class DagLink(TypedDict, total=False):
    name: Optional[str]
    hash: Mapping[str, str]
    tsize: int


class Dag(TypedDict):
    data: Mapping[str, Mapping[str, str]]
    links: Iterator[DagLink]


Service = Literal["pinata"]
# Exec type contains standardize output for ipfs commands.
# An issue here is that ipfs returns different encodings for each command, sometimes could be a string and later probably we get a json object,
# so using "output" could be fine to expect always the same field to process.
# eg. output = exec.get("output")
# ref: docs.ipfs.io/reference/cli/#ipfs
Exec = TypedDict("Exec", {"output": Any})
Pin = TypedDict("Pin", {"pins": Sequence[str]})
EdgeServices = TypedDict("Services", {"remote": Iterator[EdgeService]})

class Container(Protocol, metaclass=ABCMeta):
    """
    Docker container abstraction adapted from docker lib
    """

    @abstractmethod
    def exec_run(self, cmd: str) -> Tuple[bool, bytes]:
        ...
