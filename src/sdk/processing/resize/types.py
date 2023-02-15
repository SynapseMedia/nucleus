import dataclasses

from src.core.types import Tuple

Size = Tuple[int, int]


@dataclasses.dataclass(frozen=True)
class Sizes:
    Small: Size = (45, 67)
    Medium: Size = (230, 345)
    Large: Size = (500, 750)
