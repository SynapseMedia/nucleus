import nucleus.core.subprocess as subprocess

from nucleus.core.types import Command, Sequence, StdOut, Any


class NodeJs(Command):
    cmd: str
    args: str

    def __init__(self, cmd: str, *args: Sequence[str]):
        self.cmd = cmd
        self.args = " ".join(args)  # type: ignore

    def __str__(self) -> str:
        return f"npm run {self.cmd} -- {self.args} --enc=json"

    def __call__(self, *args: Any) -> StdOut:
        """Start a subprocess call based on class command definition.
        The command execution its based on the string representation of the class.

        :return: standard output collected from nodejs process
        :rtype: Process
        """
        call = subprocess.call(str(self))
        return call.communicate(*args)
