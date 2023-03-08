from __future__ import annotations

import src.sdk.processing.transform as transform
import src.sdk.processing.transcode as transcode
import src.sdk.exceptions as exceptions

from src.core.types import Path, Any, Mapping
from src.sdk.harvest.model import Media

from .transform import Image as ImageInput
from .transcode import FilterableStream as VideoInput
from .types import Engine, Processable

from .transcode.constants import (
    DEFAULT_PRESET,
    DEFAULT_VIDEO_BITRATE,
    DEFAULT_AUDIO_CODEC,
    DEFAULT_CRF,
    DEFAULT_KEY_MIN,
    DEFAULT_GOP,
    DEFAULT_SC_THRESHOLD,
)


class Video(Engine):
    """Video engine to support low level transcoding using ffmpeg
    ref: https://github.com/kkroening/ffmpeg-python
    """

    _type: str
    _path: Path
    _input: VideoInput
    _options: Mapping[str, Any]

    def __enter__(self):
        self._input = transcode.input(self._path, **self._options)
        return self

    def output(self, path: Path, **kwargs: Any) -> Media[Path]:
        try:
            # We generate the expected path after transcode
            self._input.output(path, **kwargs).run()  # type: ignore
            return Media(route=path, type=self._type)
        except Exception as e:
            # Standard exceptions raised
            raise exceptions.ProcessingException(str(e))


class Stream(Video):
    """Streaming engine to support streaming transcoding
    ref: https://github.com/kkroening/ffmpeg-python
    """

    _type: str
    _path: Path
    _input: VideoInput
    _options: Mapping[str, Any]

    def __init__(self, media: Processable):
        # extension_path = media.route.extension()
        super().__init__(media)
        self._options = {
            "y": "",
            "c:a": DEFAULT_AUDIO_CODEC,
            "b:a": DEFAULT_VIDEO_BITRATE,
            "crf": DEFAULT_CRF,
            "preset": DEFAULT_PRESET,
            "keyint_min": DEFAULT_KEY_MIN,
            "g": DEFAULT_GOP,
            "sc_threshold": DEFAULT_SC_THRESHOLD,
        }  # default options

    def output(self, path: Path, **kwargs: Any) -> Media[Path]:
        # check file output extension and get corresponding preset
        extension: str = path.extension()
        # get protocol based on extension output
        preset = transcode.protocol(extension)
        return super().output(path, **{**preset, **kwargs})


class Image(Engine):
    """Image engine to support image processing using Pillow
    ref: https://pillow.readthedocs.io/en/stable/reference/Image.html
    """

    _type: str
    _path: Path
    _input: ImageInput
    _options: Mapping[str, Any]

    def __enter__(self):
        self._input = transform.input(self._path, **self._options)
        return self

    def output(self, path: Path, **kwargs: Any) -> Media[Path]:
        # We generate the expected path after processing
        try:
            self._input.save(path, **kwargs)
            return Media(route=path, type=self._type)
        except Exception as e:
            # Standard exceptions raised
            raise exceptions.ProcessingException(str(e))


__all__ = ("Video", "Image", "Stream")
