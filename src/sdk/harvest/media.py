from src.core.types import Literal
from .model import Collectable


class Stream(Collectable):
    type: Literal["stream"] = "stream"


class Video(Collectable):
    type: Literal["video"] = "video"


class Image(Collectable):
    type: Literal["image"] = "image"


__all__ = ("Stream", "Image", "Video")
