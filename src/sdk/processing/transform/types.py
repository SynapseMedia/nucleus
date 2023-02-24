import dataclasses
import PIL.Image as PIL

from src.core.types import Tuple

Size = Tuple[int, int]
Image = PIL.Image


@dataclasses.dataclass(frozen=True)
class Sizes:
    small: Size = (45, 67)
    medium: Size = (230, 345)
    large: Size = (500, 750)
