from dataclasses import dataclass
from abc import abstractmethod, ABCMeta

# Convention for importing types and constants
from ffmpeg_streaming._format import H264, VP9  # type: ignore
from ffmpeg_streaming import input as ffinput  # type: ignore
from ffmpeg_streaming._input import Input as FFInput  # type: ignore
from ffmpeg_streaming import Bitrate, Representation, Size, Format, Formats, FFProbe  # type: ignore
from src.core.types import Protocol, Any, Sequence, Path


@dataclass(frozen=True)
class Sizes:
    Q144 = Size(256, 144)
    Q240 = Size(426, 240)
    Q360 = Size(640, 360)
    Q480 = Size(854, 480)
    Q720 = Size(1280, 720)
    Q1080 = Size(1920, 1080)
    Q2k = Size(2560, 1440)
    Q4k = Size(3840, 2160)


@dataclass(frozen=True)
class BRS:
    B360 = Bitrate(276 * 1024, 128 * 1024)
    B480 = Bitrate(750 * 1024, 192 * 1024)
    B720 = Bitrate(2048 * 1024, 320 * 1024)
    B1080 = Bitrate(4096 * 1024, 320 * 1024)
    B2k = Bitrate(6144 * 1024, 320 * 1024)
    B4k = Bitrate(17408 * 1024, 320 * 1024)


@dataclass(frozen=True)
class Representations:
    R360p = Representation(Sizes.Q360, BRS.B360)
    R480p = Representation(Sizes.Q480, BRS.B480)
    R720p = Representation(Sizes.Q720, BRS.B720)
    R1080p = Representation(Sizes.Q1080, BRS.B1080)
    R2k = Representation(Sizes.Q2k, BRS.B2k)
    R4k = Representation(Sizes.Q4k, BRS.B4k)


class VideoInput:
    """Adapter to give control over FFmpeg input.

    This class is designed to process one video file at time
    """

    _media: FFInput
    _probe: FFProbe
    _path: Path

    def __init__(self, input_file: Path, **options: Any):
        self._path = input_file
        self._probe = FFProbe(input_file)
        self._media = ffinput(input_file, **options)

    def get_path(self) -> Path:
        """Return current input directory

        :return: Directory string representation
        :rtype: Directory
        """
        return self._path

    def get_media(self) -> FFInput:
        """Return current file FFMPEG input

        :return" FFMPEG wrapped file
        :rtype: FFInput
        """
        return self._media

    def get_size(self) -> Size:
        """Return video size

        :return: Video size from input file
        :rtype: Size
        """
        return self._probe.video_size

    def get_duration(self) -> float:
        """Get video time duration

        :param input_file: input path
        :return: duration in seconds
        :rtype: float
        """

        format_ = self._probe.format()
        return float(format_.get("duration", 0))


class Streaming(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, input: VideoInput):
        ...

    @abstractmethod
    def set_representations(self, repr: Sequence[Representation]) -> None:
        """Add quality representation to current input
        : param repr: representation to be used on transcode process
        :return: None
        """
        ...

    @property
    @abstractmethod
    def codec(self) -> Format:
        """Return specific format codec based on protocol streaming

        This format is selected based on performance
        eg:
            mp4 -> HLS -> h264 is better in performance than mp4 -> DASH -> vp9 and vice versa

        """
        ...

    @abstractmethod
    def transcode(self, output_dir: Path) -> None:
        """Start transcoding process based on conf

        :param output_dir: Directory where to write output
        :return: None
        """
        ...


__all__ = ("H264", "VP9", "Format", "Formats")
