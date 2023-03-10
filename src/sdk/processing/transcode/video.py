from src.core.types import Any, Path #, Command
from .nodes import Video

def input(path: Path, **options: Any) -> Video:
    """Video node factory.

    :param path: Path to video
    :return: Video object
    :rtype: Video
    """
    return Video(path, **options)  # type: ignore

