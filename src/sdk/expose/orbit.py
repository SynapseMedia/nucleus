import asyncio
import src.core.subprocess as subprocess
from src.core.types import Sequence


async def migrate(collectors: Sequence[str], recreate: bool = False) -> None:
    """Spawn nodejs migrate to orbitdb subprocess

    :param collectors: list of collectors names to migrate into orbit
    :param recreate: if recreate equal True new orbit repo is created else use existing
    :return: None since is just a subprocess call
    :rtype: None
    """

    # Formulate params
    recreate_param = recreate and "-g" or ""
    commands = map(
        lambda r: subprocess.NodeJs(
            "migrate", *(recreate_param, f"--key={r}", f"--source={r}")
        ),
        collectors ,
    )

    process_list = [command() for command in commands]
    await asyncio.gather(*process_list)
