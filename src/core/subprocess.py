import asyncio
import src.core.logger as logger
import asyncio.subprocess as sub

# Convention for importing types
from src.core.types import Command, Sequence


class Subprocess(Command):
    cmd: str
    args: str

    def __init__(self, cmd: str, *args: Sequence[str]):
        self.cmd = cmd
        self.args = " ".join(*args)

    def __str__(self) -> str:
        return f"npm run {self.cmd} -- {self.args} --enc=json"

    async def __call__(self) -> sub.Process:
        """Start an async subprocess cmd

        :return: subprocess asyncio shell
        :rtype: Process
        """
        proc = await asyncio.create_subprocess_shell(str(self))
        stdout, stderr = await proc.communicate()

        if stdout:
            logger.log.info(f"[stdout]\n{stdout.decode()}")
        if stderr:
            logger.log.error(f"[stderr]\n{stderr.decode()}")
        return proc


async def migrate(sources: Sequence[str], recreate: bool = False) -> None:
    """Spawn nodejs subprocess

    :param sources: list of sources to migrate into orbit
    :param recreate: if recreate equal True new orbit repo is created else use existing
    :return: None since is just a subprocess call
    :rtype: None
    """

    # Formulate params
    recreate_param = recreate and "-g" or ""
    commands = map(
        lambda r: Subprocess(
            "migrate", (recreate_param, f"--key={r}", f"--source={r}")
        ),
        sources,
    )

    process_list = [command() for command in commands]
    await asyncio.gather(*process_list)
