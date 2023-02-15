import contextlib
import src.core.exceptions as exceptions

# Convention for importing types and constants
from ffmpeg_streaming._input import Input as FFInput  # type: ignore
from ffmpeg_streaming import input as ffinput, FFProbe  # type: ignore


from src.core.types import Iterator, Any, Mapping, Sequence, Path
from .types import Input, Representation, Representations as REPR, Size, Sizes
from .constants import MAX_MUXING_QUEUE_SIZE


class VideoInput(Input):
    """Protocol to give control over FFmpeg input.

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


def quality(size: Size) -> Sequence[Representation]:
    """Return quality list of appropriated representations based on `size`.

    Blocked upscale and locked downscale allowed for each defined quality
    :param size: master video size to match appropriate representation
    :return: list of appropriate representations based on requested quality
    :rtype: Sequence[Representation]
    :raises InvalidVideoQuality: if size not match any allowed representations
    """

    # Video quality representations allowed by size
    representations: Mapping[Size, Sequence[Representation]] = {
        Sizes.Q480: (REPR.R360p, REPR.R480p),
        Sizes.Q720: (REPR.R360p, REPR.R480p, REPR.R720p),
        Sizes.Q1080: (REPR.R360p, REPR.R480p, REPR.R720p, REPR.R1080p),
        Sizes.Q2k: (REPR.R360p, REPR.R480p, REPR.R720p, REPR.R1080p, REPR.R2k),
        Sizes.Q4k: (
            REPR.R360p,
            REPR.R480p,
            REPR.R720p,
            REPR.R1080p,
            REPR.R2k,
            REPR.R4k,
        ),
    }

    if size not in representations:
        raise exceptions.InvalidVideoQuality()
    return representations[size]


@contextlib.contextmanager
def input(input_file: Path, **options: Any) -> Iterator[Input]:
    """Factory ffmpeg input interface from file

    :param input_file: Path to video
    :return: Input interface
    :rtype: Input
    """
    yield VideoInput(
        input_file,  # file path to process
        max_muxing_queue_size=MAX_MUXING_QUEUE_SIZE,
        **options
    )
