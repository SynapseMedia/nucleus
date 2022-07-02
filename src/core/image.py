from PIL.Image import Image, open
from typing import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from .exceptions import InvalidImageSize
from .types import Directory


@dataclass(frozen=True)
class Size:
    Small = (45, 67)
    Medium = (230, 345)
    Large = (500, 750)


@contextmanager
def input(input_image: Directory) -> Iterator[Image]:
    """
    Factory Image
    :param input_image: Path to image
    :return: PIL Image object
    :rtype: Image
    :raises InvalidImageSize
    """

    with open(input_image) as image:
        # input ratio size
        w, h = image.size
        # ratio height should be major than width
        is_h_less_than_w = h < w
        # input image is smaller than "master" 
        is_input_less_than_master = any(x < y for x, y in zip(image.size, Size.Large))
        
        if is_h_less_than_w or is_input_less_than_master: 
            # Invalid image ratio height should be major than width
            raise InvalidImageSize()
        
        yield image
