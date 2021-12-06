import contextlib
from ffmpeg_streaming import Formats, Bitrate, Representation, Size, input
from tqdm import tqdm


@contextlib.contextmanager
def progress():
    """Render tqdm progress bar."""
    with tqdm(total=100) as bar:
        def handler(ffmpeg, duration, time_, time_left, process):
            per = round(time_ / duration * 100)
            bar.update(per)

        yield handler


def get_representations(quality) -> list:
    """
    Return representation list based on`quality`.
    Blocked upscale and locked downscale allowed for each defined quality.
    @param quality:
    @return list of representations based on requested quality
    """
    _144p = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
    _240p = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
    _360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
    _2k = Representation(Size(2560, 1440), Bitrate(6144 * 1024, 320 * 1024))
    _4k = Representation(Size(3840, 2160), Bitrate(17408 * 1024, 320 * 1024))

    return {
        '720p': [_144p, _240p, _360p, _480p, _720p],
        '1080p': [_144p, _240p, _360p, _480p, _720p, _1080p],
        '2k': [_144p, _240p, _360p, _480p, _720p, _1080p, _2k],
        '4k': [_144p, _240p, _360p, _480p, _720p, _1080p, _2k, _4k]
    }.get(quality.lower())


def to_dash(input_file, quality, output_dir):
    """
    Transcode movie file to dash
    :param input_file:
    :param quality:
    :param output_dir
    :return: new file format dir
    """
    with progress() as progress_handler:
        video = input(input_file)
        dash = video.dash(Formats.h264())
        dash.representations(*get_representations(quality))
        dash.output(output_dir, monitor=progress_handler)

    return output_dir
