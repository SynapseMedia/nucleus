from __future__ import annotations

import src.sdk.processing.stream as stream
import src.sdk.processing.transform as transform
import src.sdk.processing.transcode as transcode

from src.core.types import Path, Any, Dict
from src.sdk.harvest.model import Media

from .transform import Image as ImageInput
from .stream import Streaming as StreamInput
from .transcode import FilterableStream as VideoInput
from .types import Engine


class StreamEngine(Engine):
    """Streaming engine to support streaming transcoding using StreamGear
    ref: https://abhitronix.github.io/vidgear/latest/gears/streamgear/ssm/usage/
    """

    _type: str
    _path: Path
    _input: StreamInput
    _options: Dict[str, Any]

    def __enter__(self):
        # override generic engine enter
        self._input = stream.input(self._path, **self._options)
        return self

    def __exit__(self, *args: Any):
        self._input.terminate()

    def output(self, path: Path) -> Media:
        # We generate the expected path after transcode
        self._input.output(path).transcode()
        return Media(route=path, type=self._type)


class VideoEngine(Engine):
    """Video engine to support low level transcoding using ffmpeg
    ref: https://github.com/kkroening/ffmpeg-python
    """

    _type: str
    _path: Path
    _input: VideoInput
    _options: Dict[str, Any]

    def __enter__(self):
        self._input = transcode.input(self._path, **self._options)
        return self

    def output(self, path: Path) -> Media:
        # We generate the expected path after transcode
        self._input.output(path).run()  # type: ignore
        return Media(route=path, type=self._type)


class ImageEngine(Engine):
    """Image engine to support image processing using Pillow
    ref: https://pillow.readthedocs.io/en/stable/reference/Image.html
    """

    _type: str
    _path: Path
    _input: ImageInput
    _options: Dict[str, Any]

    def __enter__(self):
        self._input = transform.input(self._path, **self._options)
        return self

    def output(self, path: Path) -> Media:
        # We generate the expected path after processing
        self._input.save(path)
        return Media(route=path, type=self._type)


__all__ = ("VideoEngine", "ImageEngine", "StreamEngine")
