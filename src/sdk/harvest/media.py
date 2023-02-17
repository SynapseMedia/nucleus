from src.core.types import Literal
from .types import Media


class Video(Media):
    type: Literal["video"] = "video"


class Image(Media):
    type: Literal["image"] = "image"
