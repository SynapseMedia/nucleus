from contextlib import contextmanager
from ffmpeg_streaming import input as _input

from ... import logger
from ...constants import MAX_MUXING_QUEUE_SIZE, HLS_FORMAT, DASH_FORMAT
from ...exception import InvalidVideoQuality
from .util import get_video_size, get_reverse_quality




# TODO add tests
def quality(input_file: str):
    """Return quality from video file

    :param input_file: Path to video file
    :return video Size
    :throw InvalidVideoQuality
    """
    video_size = get_video_size(input_file)
    matched_resolution = get_reverse_quality(video_size.width)

    if not matched_resolution:
        raise InvalidVideoQuality()
    return matched_resolution


def representation(quality):
    """Return representation list based on`quality`.
    Blocked upscale and locked downscale allowed for each defined quality

    :param quality:
    :return list of representations based on requested quality
    :rtype: list
    """
    return {
        "360p": [REPR.R360p],
        "480p": [REPR.R360p, REPR.R480p],
        "720p": [REPR.R360p, REPR.R480p, REPR.R720p],
        "1080p": [REPR.R360p, REPR.R480p, REPR.R720p, REPR.R1080p],
        "2k": [REPR.R360p, REPR.R480p, REPR.R720p, REPR.R1080p, REPR.R2k],
        "4k": [REPR.R360p, REPR.R480p, REPR.R720p, REPR.R1080p, REPR.R2k, REPR.R4k],
    }.get(quality.lower())


@contextmanager
def input(input_file: str):
    """
    Factory Video
    :param input_image: Path to image
    :return: Input video object
    :rtype: Input
    """
    yield _input(input_file, max_muxing_queue_size=MAX_MUXING_QUEUE_SIZE)


# TODO write tests
def codec(protocol: str):
    """Resolve codec handler from protocol name

    :param protocol: HLS | DASH
    :return: handler function for codec
    :rtype: function
    """
    protocols = {HLS_FORMAT: to_hls, DASH_FORMAT: to_dash}

    if protocol not in protocols:
        logger.log.error("Invalid protocol provided. Please try using `hls` or `dash`")
        return None
    return protocols[protocol]
