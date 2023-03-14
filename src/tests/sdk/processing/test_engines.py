import src.sdk.processing as processing

from mock import patch
from src.core.types import Path, Any
from src.sdk.harvest import Video, Image
from src.sdk.harvest.model import Media


class MockImage:
    def save(self, path: Path, **kwargs: Any):
        return Media(route=path, type="test")


class MockVideo:
    def save(self, path: Path, **kwargs: Any):
        return Media(route=path, type="test")


def test_dispatch_engine(mock_local_video_path: Path, mock_local_image_path: Path):
    """Should dispatch the right engine based on media"""
    video = Video(route=mock_local_video_path)
    image = Image(route=mock_local_image_path)

    video_engine = processing.engine(video)
    image_engine = processing.engine(image)

    assert isinstance(video_engine, processing.Video)
    assert isinstance(image_engine, processing.Image)


def test_video_engine(mock_local_video_path: Path):
    """Should start a valid transcoding process using VideoEngine returning a valid output"""
    with patch("src.sdk.processing.process.Video") as mock:

        mock.return_value = MockVideo()
        media = Video(route=mock_local_video_path)

        # Video processing using call to pass input args
        output = Path("video.mp4")
        video = processing.engine(media)
        media = video.save(output)

        # Validate output
        assert media.route == output
        assert isinstance(media, Media)


def test_image_engine(mock_local_image_path: Path):
    """Should start a valid transform process using ImageEngine returning a valid output"""
    with patch("src.sdk.processing.process.Image") as mock:

        mock.return_value = MockImage()
        media = Image(route=mock_local_image_path)

        output = Path("image.jpg")
        # expected pillow adapter
        image = processing.engine(media)
        media = image.save(output)

        # Validate output
        assert media.route == output
        assert isinstance(media, Media)
