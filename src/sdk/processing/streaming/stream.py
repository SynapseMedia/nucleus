from src.core.types import Any, Path
from .types import Input


def input(input_file: Path, **options: Any) -> Input:
    """Factory ffmpeg input interface from file

    :param input_file: Path to video
    :return: Input interface
    :rtype: Input
    """
    return Input(input_file, **options)  # type: ignore
