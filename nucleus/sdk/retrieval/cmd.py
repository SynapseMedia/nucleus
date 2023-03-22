from nucleus.core.types import Command, Sequence
from .nodejs import NodeJs


def migrate(*args: Sequence[str]) -> Command:
    """Spawn nodejs subprocess to migrate data to orbitdb.

    :return: command to execute
    :rtype: Command
    """
    return NodeJs("migrate", *args)
