import dataclasses
import PIL.Image as PIL

from src.core.types import Tuple

Size = Tuple[int, int]
Input = PIL.Image


@dataclasses.dataclass(frozen=True)
class Sizes:
    Small: Size = (45, 67)
    Medium: Size = (230, 345)
    Large: Size = (500, 750)
