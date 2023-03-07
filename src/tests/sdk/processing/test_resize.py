import src.sdk.processing.transform as transform

from src.core.types import Path


root_dir = "src/tests/_mock/files/"
image_dir_771 = Path(f"{root_dir}771x900.jpg")
image_dir_255 = Path(f"{root_dir}255x255.jpg")
image_dir_638 = Path(f"{root_dir}638x400.jpg")


def test_valid_input():
    """Should success for valid input image"""
    with transform.input(image_dir_771) as img:
        w, h = img.size
        assert w == 771
        assert h == 900
