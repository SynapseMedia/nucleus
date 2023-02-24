import ffmpeg  # type: ignore

from src.core.types import Any, Path
from .types import FilterableStream


def input(input_file: Path, **options: Any) -> FilterableStream:
    """Factory ffmpeg input interface from file path.
    ref: https://github.com/kkroening/ffmpeg-python

    :param input_file: Path to video
    :return: FilterableStream object
    :rtype: FilterableStream
    """
    return ffmpeg.input(input_file, **options)  # type: ignore
