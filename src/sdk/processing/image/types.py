from dataclasses import dataclass
from src.core.types import Tuple
from PIL.Image import Resampling

Size = Tuple[int, int]

@dataclass
class Coord:
    top: int
    right: int
    bottom: int
    left: int


__all__ = ("Size", "Coord", "Resampling")
