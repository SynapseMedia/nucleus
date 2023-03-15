from src.core.types import Setting, Preset
from .types import Coord, Resampling

"""All these settings are defined by pillow library.
Option classes should be named in correspondence to the methods of the Pillow Image object and using the Python class naming convention.
Underneath each class is parsed as a method to setup pillow image object.
ref: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize

eg:
    # after parsing
    class RemapPalette(Option) = image.remap_palette(...) 
        ...   
    

"""


class Crop(Setting):
    """Crop image
    ref: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.crop
    """

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
    """Resize image
    ref: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize
    """

    def __init__(self, width: int, height: int):
        self._size = [width, height]
        self._box = (0, 0, *self._size)
        self._resample = Resampling.BICUBIC

    def crop(self, box: Coord):
        self._box = (box.left, box.top, box.right, box.bottom)

    def resample(self, resample: Resampling):
        self._resample = resample

    def __iter__(self) -> Preset:
        yield "size", self._size
        yield "resample", self._resample
        yield "box", self._box


__all__ = ("Crop", "Resize")
