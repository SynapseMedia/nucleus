# Convention for importing types
from src.core.types import Command, Sequence
from .ipc import IPC


class NodeJs(Command):
    cmd: str
    args: str

    def __init__(self, cmd: str, *args: Sequence[str]):
        self.cmd = cmd
        self.args = " ".join(args)  # type: ignore

    def __str__(self) -> str:
        return f"npm run {self.cmd} -- {self.args} --enc=json"

    def __call__(self) -> IPC:
        """Start a subprocess call based on class command definition.
        The command execution its based on the string representation of the class.

        :return: Process running script
        :rtype: Process
        """

        return IPC(str(self))
