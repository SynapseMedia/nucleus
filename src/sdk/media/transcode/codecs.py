from ffmpeg_streaming import Formats, FFProbe, Bitrate, Representation, Size, input
from ...exception import InvalidVideoQuality
from ...constants import HLS_TIME, MAX_MUXING_QUEUE_SIZE, HLS_FORMAT, DASH_FORMAT
from src.sdk import logger, util
import datetime
import sys


class Sizes:
    Q144 = Size(256, 144)
    Q240 = Size(426, 240)
    Q360 = Size(640, 360)
    Q480 = Size(854, 480)
    Q720 = Size(1280, 720)
    Q1080 = Size(1920, 1080)
    Q2k = Size(2560, 1440)
    Q4k = Size(3840, 2160)


class BRS:
    B360 = Bitrate(276 * 1024, 128 * 1024)
    B480 = Bitrate(750 * 1024, 192 * 1024)
    B720 = Bitrate(2048 * 1024, 320 * 1024)
    B1080 = Bitrate(4096 * 1024, 320 * 1024)
    B2k = Bitrate(6144 * 1024, 320 * 1024)
    B4k = Bitrate(17408 * 1024, 320 * 1024)


class REPR:
    R360p = Representation(Sizes.Q360, BRS.B360)
    R480p = Representation(Sizes.Q480, BRS.B480)
    R720p = Representation(Sizes.Q720, BRS.B720)
    R1080p = Representation(Sizes.Q1080, BRS.B1080)
    R2k = Representation(Sizes.Q2k, BRS.B2k)
    R4k = Representation(Sizes.Q4k, BRS.B4k)


def progress(_, duration, time_, time_left, *args, **kwargs):
    """Render tqdm progress bar."""
    sys.stdout.flush()
    per = round(time_ / duration * 100)
    sys.stdout.write(
        "\rTranscoding...(%s%%) %s left [%s%s]"
        % (
            per,
            datetime.timedelta(seconds=int(time_left)),
            "#" * per,
            "-" * (100 - per),
        )
    )


# TODO add tests
def get_new_video_quality(video: str):
    """
    Return quality from video file
    :param video: Path to video file
    :return video Size
    :throw InvalidVideoQuality
    """
    ffprobe = FFProbe(video)
    video_size = ffprobe.video_size
    logger.log.info(f"Current video quality: {video_size}")

    reversal_sizes = reversed(
        (
            (Sizes.Q360, "360p"),
            (Sizes.Q480, "480p"),
            (Sizes.Q720, "720p"),
            (Sizes.Q1080, "1080p"),
            (Sizes.Q2k, "2k"),
            (Sizes.Q4k, "4k"),
        )
    )

    matched_new_resolution = next(
        (eq for res, eq in reversal_sizes if res.width <= video_size.width), None
    )

    logger.log.info(f"Match quality: {matched_new_resolution}")
    if matched_new_resolution:
        return matched_new_resolution
    raise InvalidVideoQuality()


def get_representations(quality):
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


def to_dash(input_file: str, output_dir: str):
    """Transcode movie file to DASH and store file in output directory

    :param input_file: Current file path
    :param output_dir: New file path
    :return: new file format dir
    :rtype: str
    """
    video = input(input_file, max_muxing_queue_size=MAX_MUXING_QUEUE_SIZE)
    quality = get_new_video_quality(input_file)
    current_format = util.extract_extension(input_file)
    logger.log.warn(f"Transcoding {current_format} to DASH using VP8 codec")

    dash = video.dash(Formats.vp8())
    dash.representations(*get_representations(quality))
    dash.output(output_dir, monitor=progress)
    sys.stdout.write("\n")
    return output_dir


def to_hls(input_file: str, output_dir: str):
    """Transcode movie file to HLS and store file in output directory

    :param input_file: Current file path
    :param output_dir: New file path
    :return: new file format dir
    :rtype: str
    """
    video = input(input_file, max_muxing_queue_size=MAX_MUXING_QUEUE_SIZE)
    quality = get_new_video_quality(input_file)
    current_format = util.extract_extension(input_file)
    logger.log.warn(f"Transcoding {current_format} to HLS using H264 codec")

    hls = video.hls(Formats.h264(), hls_time=HLS_TIME)
    hls.representations(*get_representations(quality))
    hls.output(output_dir, monitor=progress)
    sys.stdout.write("\n")
    return output_dir


def get_codec(protocol: str):
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
