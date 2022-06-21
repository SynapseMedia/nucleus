from PIL import Image
from contextlib import contextmanager
from dataclasses import dataclass
from .types import Directory


@dataclass(frozen=True)
class Size:
    Small = (45, 67)
    Medium = (230, 345)
    Large = (500, 750)


@contextmanager
def input(input_image: Directory):
    """
    Factory Image
    :param input_image: Path to image
    :return: PIL Image object
    :rtype: Image
    """
    yield Image.open(input_image)
