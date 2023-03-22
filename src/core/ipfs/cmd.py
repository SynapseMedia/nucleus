import json
import docker  # type: ignore
import src.core.exceptions as exceptions
import src.core.subprocess as subprocess

from src.core.types import Command, StdOut
from .constants import IPFS_CONTAINER
from .types import Sequence, Container


def get_container() -> Container:
    """Return a Container to handle docker commands

    :return: container object from docker lib
    :rtype: Container
    """
    client = docker.from_env()  # type: ignore
    return client.containers.get(IPFS_CONTAINER)  # type: ignore


class IPFS(Command):
    cmd: str
    args: str

    def __init__(self, cmd: str, *args: Sequence[str]):
        self.cmd = " ".join(cmd.split("/"))  # Parse path to commands
        self.args = " ".join(*args)

    def __str__(self) -> str:
        return f"ipfs {self.cmd} {self.args} --enc=json"

    def __call__(self) -> StdOut:
        """Execute built command in container

        :return: standard output with collected data from subprocess call to ipfs
        :rtype: StdOut
        :raises IPFSRuntimeException: if exit code > or empty output is returned from command
        """
        call = subprocess.call(str(self))
        stdout = call.communicate()

        if stdout.exit_code > 0:
            """
            The CLI will exit with one of the following values:

            0     Successful execution.
            1     Failed executions.
            """
            raise exceptions.IPFSRuntimeError(
                f"error while try to execute IPFS command: {stdout.output}"
            )

        # If not result just keep object output standard
        if not stdout.output:
            raise exceptions.IPFSRuntimeError(
                "received invalid IPFS command call output",
            )

        # StdOut type contains standardize output for ipfs commands.
        # An issue here is that ipfs returns different encodings for each
        # command, sometimes could be a string and later probably we get a json object.
        # ref: docs.ipfs.io/reference/cli/#ipfs
        try:
            json_to_dict = json.loads(stdout.output)
            return StdOut(stdout.exit_code, json_to_dict)
        except json.decoder.JSONDecodeError:
            return StdOut(stdout.exit_code, stdout.output)
