from unittest.mock import patch

import nucleus.sdk.processing as processing
from nucleus.core.types import Any, Path
from nucleus.sdk.harvest import Image, Media, Video


class MockMedia:
    def save(self, path: Path, **kwargs: Any) -> Media[Path]:
        return Media(path=path)


def test_dispatch_engine(mock_local_video_path: Path, mock_local_image_path: Path):
    """Should dispatch the right engine based on media"""
    video = Video(path=mock_local_video_path)
    image = Image(path=mock_local_image_path)

    video_engine = processing.engine(video)
    image_engine = processing.engine(image)

    assert isinstance(video_engine, processing.VideoEngine)
    assert isinstance(image_engine, processing.ImageEngine)


def test_video_engine(mock_local_video_path: Path):
    """Should start a valid transcoding process using VideoEngine returning a valid output"""
    with patch('nucleus.sdk.processing.process.VideoEngine') as mock:
        mock.return_value = MockMedia()
        media = Video(path=mock_local_video_path)

        # Video processing using call to pass input args
        output = Path('video.mp4')
        video = processing.engine(media)
        media = video.save(output)

        # Validate output
        assert media.path == output
        assert isinstance(media, Media)


def test_image_engine(mock_local_image_path: Path):
    """Should start a valid transform process using ImageEngine returning a valid output"""
    with patch('nucleus.sdk.processing.process.ImageEngine') as mock:
        mock.return_value = MockMedia()
        media = Image(path=mock_local_image_path)

        output = Path('image.jpg')
        # expected pillow adapter
        image = processing.engine(media)
        media = image.save(output)

        # Validate output
        assert media.path == output
        assert isinstance(media, Media)
