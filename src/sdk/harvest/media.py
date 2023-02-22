from src.core.types import Literal, Union
from .fields import HttpUrl, FilePath
from .model import Media


class Stream(Media):
    route: Union[HttpUrl, FilePath]
    type: Literal["stream"] = "stream"


class Video(Media):
    route: Union[HttpUrl, FilePath]
    type: Literal["video"] = "video"


class Image(Media):
    route: Union[HttpUrl, FilePath]
    type: Literal["image"] = "image"


__all__ = ("Stream", "Image", "Video")
