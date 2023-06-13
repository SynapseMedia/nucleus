from dataclasses import dataclass, field

from PIL.Image import Resampling

from nucleus.core.types import Tuple

"""
All these settings are defined by the Pillow library.
Option classes should be named according to the corresponding methods of the Pillow Image object, 
following the Python class naming convention.

During processing, the underlying option classes are parsed as a method to dynamically call the Pillow image object.
Reference: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize

For example:
    # after parsing
    class RemapPalette(Option) <= image.remap_palette(...)
        ...
"""


@dataclass(slots=True)
class Coord:
    """Represents a cartesian pixel coordinate."""

    left: int
    top: int
    right: int
    bottom: int


@dataclass(slots=True)
class Crop:
    """Crop a rectangular region from an image."""

    box: Coord

    def __iter__(self):
        yield 'box', (
            self.box.left,
            self.box.top,
            self.box.right,
            self.box.bottom,
        )


@dataclass(slots=True)
class Thumbnail:
    """Resize the image into a thumbnail."""

    _size: Tuple[int, int] = field(init=False)
    _gap: float = field(init=False)
    _resample: Resampling = field(init=False)

    width: int
    height: int

    def __post_init__(self):
        self._gap = 2.0
        self._size = (self.width, self.height)
        self._resample = Resampling.BICUBIC

    def reducing_gap(self, gap: float):
        self._gap = gap

    def resample(self, resample: Resampling):
        self._resample = resample

    def __iter__(self):
        yield 'size', self._size
        yield 'resample', self._resample
        yield 'reducing_gap', self._gap


@dataclass(slots=True)
class Resize:
    """Resize the image to a given size."""

    _size: Tuple[int, int] = field(init=False)
    _box: Tuple[int, int, int, int] = field(init=False)
    _resample: Resampling = field(init=False)

    width: int
    height: int

    def __post_init__(self):
        self._size = (self.width, self.height)
        self._box = (0, 0, *self._size)
        self._resample = Resampling.BICUBIC

    def crop(self, box: Coord):
        self._box = (box.left, box.top, box.right, box.bottom)

    def resample(self, resample: Resampling):
        self._resample = resample

    def __iter__(self):
        yield 'size', self._size
        yield 'resample', self._resample
        yield 'box', self._box


__all__ = ('Crop', 'Coord', 'Resize', 'Resampling')
