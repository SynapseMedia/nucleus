import asyncio
import src.core.subprocess as subprocess

from src.core.types import Iterator, Any
from src.sdk.harvest.types import Collector


async def migrate(collectors: Iterator[Collector], **kwargs: Any) -> None:
    """Spawn nodejs migrate to orbitdb subprocess

    :param collectors: list of collectors names to migrate into orbit
    :return: None since is just a subprocess call
    :rtype: None
    """

    # Formulate params
    commands = map(
        lambda r: subprocess.NodeJs(
            "migrate", *(f"--key={r}", f"--source={r}")
        ),
        collectors,
    )

    process_list = [command() for command in commands]
    await asyncio.gather(*process_list)
