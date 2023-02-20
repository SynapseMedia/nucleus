import src.core.exceptions as exceptions

from src.core.types import Any, Mapping, Sequence, Path
from .types import Input, Representation, Representations as REPR, Size, Sizes
from .constants import MAX_MUXING_QUEUE_SIZE


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


def input(input_file: Path, **options: Any) -> Input:
    """Factory ffmpeg input interface from file

    :param input_file: Path to video
    :return: Input interface
    :rtype: Input
    """
    return Input(
        input_file,  # file path to process
        max_muxing_queue_size=MAX_MUXING_QUEUE_SIZE,
        **options
    )
