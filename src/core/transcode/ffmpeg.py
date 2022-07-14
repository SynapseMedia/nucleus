import contextlib
import src.core.exceptions as exceptions

from src.core.types import Directory, Dict, Sequence, Iterator
from src.core.constants import MAX_MUXING_QUEUE_SIZE

# package types
from .types import REPR, Sizes, Input, Size, Representation


def quality(size: Size) -> Sequence[Representation]:
    """Return quality list of appropriated representations based on `size`.

    Blocked upscale and locked downscale allowed for each defined quality
    :param size: master video size to match appropriate representation
    :return: list of appropriate representations based on requested quality
    :rtype: tuple
    :raises InvalidVideoQuality
    """

    quality_representations: Dict[Size, Sequence[Representation]] = {
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

    if size not in quality_representations:
        raise exceptions.InvalidVideoQuality()
    return quality_representations[size]


@contextlib.contextmanager
def input(input_file: Directory) -> Iterator[Input]:
    """Factory ffmpeg input interface from file

    :param input_file: Path to video
    :return: Input interface
    :rtype: Input
    """
    yield Input(input_file, max_muxing_queue_size=MAX_MUXING_QUEUE_SIZE)
