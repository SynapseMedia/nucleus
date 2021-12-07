import contextlib
from ffmpeg_streaming import Formats, FFProbe, Bitrate, Representation, Size, input
from ...exception import InvalidVideoQuality
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


@contextlib.contextmanager
def progress():
    """Render tqdm progress bar."""

    def handler(ffmpeg, duration, time_, time_left, process):
        per = round(time_ / duration * 100)
        sys.stdout.write(
            "\rTranscoding...(%s%%) %s left [%s%s]" %
            (per, datetime.timedelta(seconds=int(time_left)), '#' * per, '-' * (100 - per))
        )
        sys.stdout.flush()

    yield handler


def get_reverse_quality(video):
    """
    Return quality from video file
    :param video: Path to video file
    :return video Size
    :throw InvalidVideoQuality
    """
    ffprobe = FFProbe(video)
    video_size = ffprobe.video_size

    reversal_sizes = {
        Sizes.Q360: '360p',
        Sizes.Q480: '480p',
        Sizes.Q720: '720p',
        Sizes.Q1080: '1080p',
        Sizes.Q2k: '2k',
        Sizes.Q4k: '4k'
    }

    if video_size in reversal_sizes:
        return reversal_sizes[video_size]
    raise InvalidVideoQuality()


def get_representations(quality) -> list:
    """
    Return representation list based on`quality`.
    Blocked upscale and locked downscale allowed for each defined quality
    :param quality:
    :return list of representations based on requested quality
    """
    _360p = Representation(Sizes.Q360, BRS.B360)
    _480p = Representation(Sizes.Q480, BRS.B480)
    _720p = Representation(Sizes.Q720, BRS.B720)
    _1080p = Representation(Sizes.Q1080, BRS.B1080)
    _2k = Representation(Sizes.Q2k, BRS.B2k)
    _4k = Representation(Sizes.Q4k, BRS.B4k)

    return {
        "720p": [_360p, _480p, _720p],
        "1080p": [_360p, _480p, _720p, _1080p],
        "2k": [_360p, _480p, _720p, _1080p, _2k],
        "4k": [_360p, _480p, _720p, _1080p, _2k, _4k],
    }.get(quality.lower())


def to_dash(input_file, output_dir):
    """
    Transcode movie file to dash
    :param input_file:
    :param output_dir
    :return: new file format dir
    """
    with progress() as progress_handler:
        video = input(input_file)
        quality = get_reverse_quality(input_file)

        dash = video.dash(Formats.vp9())
        dash.representations(*get_representations(quality))
        dash.output(output_dir, monitor=progress_handler)

    return output_dir


def to_hls(input_file, output_dir):
    """
    Transcode movie file to hls
    :param input_file:
    :param output_dir
    :return: new file format dir
    """
    with progress() as progress_handler:
        video = input(input_file)
        quality = get_reverse_quality(input_file)

        hls = video.hls(Formats.h264())
        hls.representations(*get_representations(quality))
        hls.output(output_dir, monitor=progress_handler)

    return output_dir
