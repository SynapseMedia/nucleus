from contextlib import contextmanager

from ...constants import MAX_MUXING_QUEUE_SIZE
from ...exception import InvalidVideoQuality, InvalidVideoProtocol
from . import REPR, Quality, Sizes, Input, Protocol
from .codecs import HLS, DASH


def quality(input: Input):
    """Return quality from video file

    :param input: FFmpeg interface
    :return: quality based on video size
    :rtype: Quality
    :throw InvalidVideoQuality
    """
    video_size = input.get_video_size()
    quality_sizes = {
        Sizes.Q360: Quality.Q360,
        Sizes.Q480: Quality.Q480,
        Sizes.Q720: Quality.Q720,
        Sizes.Q1080: Quality.Q1080,
        Sizes.Q2k: Quality.Q2k,
        Sizes.Q4k: Quality.Q4k,
    }

    if video_size not in quality_sizes:
        raise InvalidVideoQuality()
    return quality_sizes[video_size]


def representation(_quality: Quality):
    """Return representation list based on`quality`.

    Blocked upscale and locked downscale allowed for each defined quality
    :param quality: quality to match representation.
    :return: list of representations based on requested quality
    :rtype: tuple
    """

    quality_representations = {
        Quality.Q360: (REPR.R360p),
        Quality.Q480: (REPR.R360p, REPR.R480p),
        Quality.Q720: (REPR.R360p, REPR.R480p, REPR.R720p),
        Quality.Q1080: (REPR.R360p, REPR.R480p, REPR.R720p, REPR.R1080p),
        Quality.Q2k: (REPR.R360p, REPR.R480p, REPR.R720p, REPR.R1080p, REPR.R2k),
        Quality.Q4k: (
            REPR.R360p,
            REPR.R480p,
            REPR.R720p,
            REPR.R1080p,
            REPR.R2k,
            REPR.R4k,
        ),
    }

    if _quality not in quality_representations:
        raise InvalidVideoQuality()
    return quality_representations[_quality]


@contextmanager
def input(input_file: str):
    """
    Factory input FFmpeg
    :param input_image: Path to image
    :return: FFmpeg interface
    :rtype: FFmpeg
    """
    yield Input(input_file, max_muxing_queue_size=MAX_MUXING_QUEUE_SIZE)


@contextmanager
def codec(protocol: Protocol):
    """Resolve codec handler from protocol name

    :param protocol: expected protocol to process video eg. HLS | DASH
    :return: Codec type based on protocol
    :rtype: Codec
    """

    protocols = {Protocol.HLS: HLS, Protocol.DASH: DASH}
    if protocol not in protocols:
        raise InvalidVideoProtocol()
    return protocols[protocol]
