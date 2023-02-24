from src.core.types import Literal, Union, Path, URL
from .model import Media


class Stream(Media):
    route: Union[URL, Path]
    type: Literal["stream"] = "stream"


class Video(Media):
    route: Union[URL, Path]
    type: Literal["video"] = "video"


class Image(Media):
    route: Union[URL, Path]
    type: Literal["image"] = "image"


__all__ = ("Stream", "Image", "Video")
