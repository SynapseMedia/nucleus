import ffmpeg  # type: ignore

from src.core.types import Any, Path
from .types import InputNode


def input(input_file: Path, **options: Any) -> InputNode:
    """Factory ffmpeg input interface from file path.
    ref: https://github.com/kkroening/ffmpeg-python

    :param input_file: Path to video
    :return: Input interface
    :rtype: Input
    """
    return ffmpeg.input(input_file, **options)  # type: ignore
