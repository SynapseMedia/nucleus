import src.sdk.harvest as harvest

from src.core.types import Path


def test_meta_partial():
    """Should return expected Meta based model"""

    meta_model = harvest.meta("MyMeta", a=(str, "hello"), b=(str, "world"))
    assert meta_model.__name__ == "MyMeta"
    # should be equal to default meta field + custom fields
    assert list(meta_model.__fields__.keys()) == [
        "name", "description", "a", "b"]


def test_video_partial():
    """Should return expected Video Media based model"""
    expected_route = Path("src/tests/_mock/files/video.mp4")
    meta_model = harvest.video(route=expected_route)
    assert meta_model.__class__.__name__ == "Video"
    assert meta_model.route == expected_route


def test_image_partial():
    """Should return expected Image Media based model"""
    expected_route = Path("src/tests/_mock/files/watchit.png")
    meta_model = harvest.image(route=expected_route)
    assert meta_model.__class__.__name__ == "Image"
    assert meta_model.route == expected_route
