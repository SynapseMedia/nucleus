from src.core.types import Literal
from .model import Media


class Stream(Media):
    type: Literal["stream"] = "stream"


class Video(Media):
    type: Literal["video"] = "video"


class Image(Media):
    type: Literal["image"] = "image"
