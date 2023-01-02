import asyncio

# Convention for importing types
from src.core.types import Command, Sequence, Iterator


class NodeJs(Command):
    cmd: str
    args: str

    def __init__(self, cmd: str, *args: Sequence[str]):
        self.cmd = cmd
        self.args = " ".join(*args)

    def __str__(self) -> str:
        return f"npm run {self.cmd} -- {self.args} --enc=json"

    async def __call__(self) -> str:
        """Start an async subprocess cmd

        :return: subprocess asyncio shell
        :rtype: sub.Process
        """
        cmd = str(self)
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE
        )
        
        stdout, _ = await proc.communicate()
        return stdout.decode().strip()


def spawn(cmd: Iterator[Command]):
    """Spawn a list of subprocess.

    :param cmd: The list of commands to execute
    :return: None its just a call
    :rtype: None
    """
    # https://docs.python.org/3/library/asyncio-task.html
    loop = asyncio.get_event_loop()

    # list of sub process to exec
    commands = [c() for c in cmd]
    tasks = asyncio.gather(*commands)

    # done?
    loop.run_until_complete(tasks)
    loop.close()
