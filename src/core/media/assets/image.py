from PIL import Image
from contextlib import contextmanager
from pathlib import Path

SMALL = "small"
MEDIUM = "medium"
LARGE = "large"
SIZES = {SMALL, MEDIUM, LARGE}


class Sizes:
    Small = (45, 67)
    Medium = (230, 345)
    Large = (500, 750)


@contextmanager
def open_image(input_image: str):
    """
    Factory Image function
    :param input_image: Path to image
    :return Image object
    """
    yield Image.open(input_image)


# TODO write tests
def get_representations(size: str):
    """
    Return representation list based on`size`.
    Blocked upscale and locked downscale allowed for each defined quality
    :param size:
    :return list of representations based on requested size
    """

    return {
        SMALL: Sizes.Small,
        MEDIUM: Sizes.Medium,
        LARGE: Sizes.Large,
    }.get(size.lower())
