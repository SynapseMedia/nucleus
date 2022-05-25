from PIL import Image
from contextlib import contextmanager


@contextmanager
def input(input_image: str):
    """
    Factory Image
    :param input_image: Path to image
    :return: PIL Image object
    :rtype: Image
    """
    yield Image.open(input_image)
