from src.core.types import Any, Path
from .protocol import Streaming


def input(input_file: Path, **options: Any) -> Streaming:
    """Factory ffmpeg input interface from file

    :param input_file: Path to video
    :return: Input interface
    :rtype: Input
    """
    return Streaming(input_file, **options)  # type: ignore
