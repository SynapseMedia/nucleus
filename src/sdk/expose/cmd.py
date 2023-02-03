import src.core.subprocess as subprocess

from src.core.types import Command
from src.sdk.harvest.types import Collector


def migrate(collector: Collector) -> Command:
    """Spawn nodejs subprocess to migrate data to orbitdb.

    :param collectors: collector to migrate into orbit
    :return: Command to execute
    :rtype: Command
    """

    args = (f"--key={collector}", f"--c={collector}")
    return subprocess.Script("migrate", args)