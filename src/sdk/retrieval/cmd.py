import src.core.subprocess as subprocess

from src.core.types import Command, Sequence


def migrate(*args: Sequence[str]) -> Command:
    """Spawn nodejs subprocess to migrate data to orbitdb.

    :param collectors: collector to migrate into orbit
    :return: Command to execute
    :rtype: Command
    """

    return subprocess.Script("migrate", *args)
