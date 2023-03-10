from src.core.types import Command, Sequence
from .commands import NodeJs


def node(cmd: str, *args: Sequence[str]) -> Command:
    """Spawn nodejs subprocess .

    :param cmd: script to run based on package.json
    :return: Command to execute
    :rtype: Command
    """
    return NodeJs(cmd, *args)
