# Convention for importing types
from src.core.types import Path, Any
from .pillow import Image


def input(path: Path, **options: Any) -> Image:
    """Pillow image factory.

    :param input_image: Path to image
    :return: Image object
    :rtype: Image
    """

    return Image(path, **options)
