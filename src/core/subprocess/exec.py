from src.core.types import Command, Sequence
from .nodejs import Script


def script(cmd: str, *args: Sequence[str]) -> Command:
    """Spawn nodejs subprocess .

    :param cmd: script to run based on package.json
    :return: Command to execute
    :rtype: Command
    """
    return Script(cmd, *args)
