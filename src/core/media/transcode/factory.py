from contextlib import contextmanager

from ...constants import MAX_MUXING_QUEUE_SIZE
from ...exceptions import InvalidVideoQuality, InvalidStreamingProtocol
from . import REPR, Sizes, Input, ProtocolID, Sizes
from .protocols import HLS, DASH


def quality(size: Sizes):
    """Return quality list of appropriated representations based on `size`.

    Blocked upscale and locked downscale allowed for each defined quality
    :param size: master video size to match appropriate representation
    :return: list of appropriate representations based on requested quality
    :rtype: tuple
    :raises InvalidVideoQuality
    """

    quality_representations = {
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
        raise InvalidVideoQuality()
    return quality_representations.get(size)


# TODO write tests
@contextmanager
def input(input_file: str):
    """Factory input FFmpeg
    
    :param input_file: Path to video
    :return: Input interface
    :rtype: Input
    """
    yield Input(input_file, max_muxing_queue_size=MAX_MUXING_QUEUE_SIZE)


@contextmanager
def streaming(protocol: ProtocolID):
    """Resolve protocol handler from protocol id

    :param protocol: expected protocol to process video eg. HLS | DASH
    :return: Streaming type based on protocol
    :rtype: Streaming
    :raises InvalidStreamingProtocol
    """

    protocols = {ProtocolID.HLS: HLS, ProtocolID.DASH: DASH}
    if protocol not in protocols:
        raise InvalidStreamingProtocol()

    protocol_class = protocols.get(protocol)
    yield protocol_class()
