import nucleus.sdk.processing as processing

from mock import patch
from nucleus.core.types import Path, Any
from nucleus.sdk.harvest import Video, Image, Media, MediaType


class MockImage:
    def save(self, path: Path, **kwargs: Any) -> Media[Path]:
        return Media(route=path, type=MediaType.IMAGE)


class MockVideo:
    def save(self, path: Path, **kwargs: Any) -> Media[Path]:
        return Media(route=path, type=MediaType.VIDEO)


def test_dispatch_engine(
        mock_local_video_path: Path,
        mock_local_image_path: Path):
    """Should dispatch the right engine based on media"""
    video = Video(route=mock_local_video_path)
    image = Image(route=mock_local_image_path)

    video_engine = processing.engine(video)
    image_engine = processing.engine(image)

    assert isinstance(video_engine, processing.VideoEngine)
    assert isinstance(image_engine, processing.ImageEngine)


def test_video_engine(mock_local_video_path: Path):
    """Should start a valid transcoding process using VideoEngine returning a valid output"""
    with patch("nucleus.sdk.processing.process.VideoEngine") as mock:

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
    with patch("nucleus.sdk.processing.process.ImageEngine") as mock:

        mock.return_value = MockImage()
        media = Image(route=mock_local_image_path)

        output = Path("image.jpg")
        # expected pillow adapter
        image = processing.engine(media)
        media = image.save(output)

        # Validate output
        assert media.route == output
        assert isinstance(media, Media)
