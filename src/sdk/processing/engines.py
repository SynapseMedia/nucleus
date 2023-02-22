from src.core.types import Path, Any

from .resize import input as image_input, Image as ImageInput
from .stream import input as stream_input, Streaming as StreamInput
from .transcode import input as video_input, InputNode as VideoInput
from .types import Engine


class StreamEngine(Engine):
    """Streaming engine to support streaming transcoding using StreamGear"""

    _input: StreamInput

    def __init__(self, path: Path, **options: Any):
        self._input = stream_input(path, **options)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._input, name)

    def output(self, path: Path) -> Path:
        self._input.stream(path).transcode()
        return path


class VideoEngine(Engine):
    """Video engine to support low level transcoding using ffmpeg"""

    _input: VideoInput

    def __init__(self, path: Path, **options: Any):
        self._input = video_input(path, **options)

    def __getattr__(self, name: str) -> Any:
        """We could interact directly with ffmpeg methods
        ref: https://github.com/kkroening/ffmpeg-python
        ref: https://ffmpeg.org/ffmpeg-all.html
        """
        return getattr(self._input, name)

    def output(self, path: Path) -> Path:
        self._input.output(path).run()  # type: ignore
        return path


class ImageEngine(Engine):
    """Image engine to support image processing using Pillow"""

    _input: ImageInput

    def __init__(self, path: Path, **options: Any):
        self._input = image_input(path, **options)

    def __getattr__(self, name: str) -> Any:
        """We could interact directly with Pillow methods
        ref: https://pillow.readthedocs.io/en/stable/reference/Image.html
        """
        return getattr(self._input, name)

    def output(self, path: Path):
        self._input.save(path)
        return path


__all__ = ("VideoEngine", "ImageEngine", "StreamEngine")
