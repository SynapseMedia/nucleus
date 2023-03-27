from nucleus.core.types import Literal
from .models import Collectable


class Video(Collectable):
    type: Literal["video"] = "video"


class Image(Collectable):
    type: Literal["image"] = "image"


__all__ = ("Image", "Video")