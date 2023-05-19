import nucleus.sdk.harvest as harvest
from nucleus.core.types import Path


def test_meta_partial():
    """Should return expected Meta based model"""

    meta_model = harvest.model('MyMeta', a=(str, 'hello'), b=(str, 'world'))
    assert meta_model.__name__ == 'MyMeta'
    # should be equal to default meta field + custom fields
    assert list(meta_model.__fields__.keys()) == ['name', 'desc', 'a', 'b']


def test_video_partial():
    """Should return expected Video Media based model"""
    expected_route = Path('nucleus/tests/_mock/files/video.mp4')
    meta_model = harvest.video(path=expected_route)
    assert type(meta_model).__name__ == 'Video'
    assert meta_model.path == expected_route


def test_image_partial():
    """Should return expected Image Media based model"""
    expected_route = Path('nucleus/tests/_mock/files/watchit.png')
    meta_model = harvest.image(path=expected_route)
    assert type(meta_model).__name__ == 'Image'
    assert meta_model.path == expected_route
