from src.core.types import Setting, Preset
from .types import Coord, Size, Resampling

"""All these settings are defined by pillow library:
ref: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize

"""


class Crop(Setting):
    """Crop image"""

    def __init__(self, box: Coord):
        self._box = box

    def __iter__(self) -> Preset:
        yield "box", (
            self._box.left,
            self._box.top,
            self._box.right,
            self._box.bottom,
        )


class Resize(Setting):
    """Resize image"""

    def __init__(self, size: Size):
        self._size = size
        self._box = Coord(0, 0, *size)
        self._resample = Resampling.BICUBIC

    def crop(self, box: Coord):
        self._box = box

    def resample(self, resample: Resampling):
        self._resample = resample

    def __iter__(self) -> Preset:
        yield "size", self._size
        yield "resample", self._resample
        yield "box", self._box


__all__ = ("Crop", "Resize")
