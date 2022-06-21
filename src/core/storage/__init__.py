import json
import docker  # type: ignore
from typing import Sequence

from ..constants import IPFS_CONTAINER
from ..types import ExecResult, Command, Container
from ..exceptions import IPFSFailedExecution


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

    def __call__(self) -> ExecResult:
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
            return ExecResult(result=json_to_dict)
        except json.decoder.JSONDecodeError:
            return ExecResult(result=output.decode("utf-8"))
