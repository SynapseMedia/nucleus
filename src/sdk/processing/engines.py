from __future__ import annotations

import src.sdk.processing.transform as transform
import src.sdk.processing.transcode as transcode
import src.sdk.exceptions as exceptions

from src.core.types import Path, Any, Mapping
from src.sdk.harvest.model import Media

from .transform import Image as ImageInput
from .transcode import FilterableStream as VideoInput
from .types import Engine, Processable


class Video(Engine):
    """Video engine to support low level transcoding using ffmpeg
    ref: https://github.com/kkroening/ffmpeg-python
    """

    _type: str
    _path: Path
    _input: VideoInput
    _options: Mapping[str, Any]

    def __enter__(self):
        self._input = transcode.input(self._path)
        return self

    def output(self, path: Path) -> Media[Path]:
        try:
            # We generate the expected path after transcode
            self._input.output(path, **self._options).run()  # type: ignore
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
            "c:a": "aac",
            "crf": 0,  # The range of the CRF scale is 0–51, where 0 is lossless
            "b:a": "128k",  # apple recommends 32-160 kb/s
            # The preset determines compression efficiency and therefore
            # affects encoding speed
            "preset": "medium",
        }  # default options

    def _hls(self):
        """Presets for HLS streaming protocol

        ref: https://developer.apple.com/documentation/http_live_streaming/http_live_streaming_hls_authoring_specification_for_apple_devices
        """
        return {
            "c:v": "libx265",
            "x265-params": "lossless=1",
            "f": "hls",
            "hls_time": 10,
            "hls_list_size": 0,
            "hls_playlist_type": "vod",
            "keyint_min": 100,
            "g": 100,
            "sc_threshold": 0,
            "tag:v": "hvc1",
        }

    def output(self, path: Path) -> Media[Path]:
        self._options = {**self._hls(), **self._options}
        return super().output(path)


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

    def output(self, path: Path) -> Media[Path]:
        # We generate the expected path after processing
        try:
            self._input.save(path)
            return Media(route=path, type=self._type)
        except Exception as e:
            # Standard exceptions raised
            raise exceptions.ProcessingException(str(e))


__all__ = ("Video", "Image", "Stream")
