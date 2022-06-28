import json
import docker  # type: ignore
from typing import Sequence, TypedDict, Any, Optional, Mapping, Literal, Iterator

from ..constants import IPFS_CONTAINER
from ..types import Command, Container
from ..exceptions import IPFSFailedExecution

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


def get_container() -> Container:
    """Return a Container to handle docker commands

    :return: Container object from docker lib
    :rtype: Container
    """
    client = docker.from_env()  # type: ignore
    return client.containers.get(IPFS_CONTAINER)  # type: ignore


class CLI(Command):
    cmd: str
    args: str

    def __init__(self, cmd: str, *args: Sequence[str]):
        self.cmd = " ".join(cmd.split("/"))  # Parse path to commands
        self.args = " ".join(*args)

    def __str__(self) -> str:
        return f"ipfs {self.cmd} {self.args} --enc=json"

    def __call__(self) -> Exec:
        """Execute built command in container

        :return: Output dict from command. ref: https://docs.ipfs.io/reference/cli/
        :raises IPFSFailedExecution
        :rtype: Output
        """
        container = get_container()
        code, output = container.exec_run(str(self))

        if code > 0:
            """
            The CLI will exit with one of the following values:

            0     Successful execution.
            1     Failed executions.
            """
            raise IPFSFailedExecution(output.decode("utf-8"))

        # If not result just keep object output standard
        if not output:
            raise IPFSFailedExecution("Invalid IPFS command call output")

        try:
            json_to_dict = json.loads(output)
            return Exec(output=json_to_dict)
        except json.decoder.JSONDecodeError:
            return Exec(output=output.decode("utf-8"))
