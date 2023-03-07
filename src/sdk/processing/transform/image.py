import PIL.Image as PIL

# Convention for importing types
from src.core.types import Path, Any
from .types import Image


def input(input_image: Path, **options: Any) -> Image:
    """Factory Image

    :param input_image: Path to image
    :return: Image object
    :rtype: Image
    """

    return PIL.open(input_image, **options)
