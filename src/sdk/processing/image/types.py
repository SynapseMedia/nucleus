from dataclasses import dataclass
from PIL.Image import Resampling

@dataclass
class Coord:
    left: int
    top: int
    right: int
    bottom: int


__all__ = ("Coord", "Resampling")
