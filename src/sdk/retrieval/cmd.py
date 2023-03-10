import src.core.subprocess as subprocess

from src.core.types import Command, Sequence


def migrate(*args: Sequence[str]) -> Command:
    """Spawn nodejs subprocess to migrate data to orbitdb.

    :return: Command to execute
    :rtype: Command
    """
    return subprocess.node("migrate", *args)
