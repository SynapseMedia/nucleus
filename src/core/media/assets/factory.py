from PIL import Image
from contextlib import contextmanager

SMALL = 0
MEDIUM = 1
LARGE = 2
SIZES = {SMALL, MEDIUM, LARGE}


class Size:
    Small = (45, 67)
    Medium = (230, 345)
    Large = (500, 750)


@contextmanager
def input(input_image: str):
    """
    Factory Image
    :param input_image: Path to image
    :return: PIL Image object
    :rtype: Image
    """
    yield Image.open(input_image)


# TODO write tests
def representation(size: int):
    """Return representation based on`size`.

    Blocked upscale and locked downscale allowed for each defined quality
    :param size: integer representation for SIZE
    :return: list of representations based on requested size
    :rtype: tuple
    """

    if size not in SIZES:
        raise

    return {
        SMALL: Size.Small,
        MEDIUM: Size.Medium,
        LARGE: Size.Large,
    }.get(size.lower())
