import os
import subprocess as sub

# Convention for importing types
from src.core.types import Command, Sequence
from .types import Process


class Script(Command):
    cmd: str
    args: str

    def __init__(self, cmd: str, *args: Sequence[str]):
        self.cmd = cmd
        self.args = " ".join(*args)

    def __str__(self) -> str:
        return f"npm run {self.cmd} -- {self.args} --enc=json"

    def __call__(self) -> Process:
        """Start a subprocess call based on class command definition.
        The command execution its based on the string representation of the class.

        :return: Process running script
        :rtype: Process
        """

        #TODO try with asyncio
        return sub.Popen(
            str(self),
            stdout=sub.PIPE,
            stderr=sub.PIPE,
            shell=True,
            # bypass running environment
            env=os.environ.copy(),
        )
