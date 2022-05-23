import sys
import datetime


from ffmpeg_streaming import FFProbe


def get_video_size(input_file: str):
    ffprobe = FFProbe(input_file)
    return ffprobe.video_size


# TODO write tests
# TODO add docs
def get_reverse_quality(width):
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

    # Reverse match appropriate video resolution
    _, matched_resolution = next(filter(lambda r, _: r.width <= width, reversal_sizes))
    return matched_resolution


# TODO add test_has_valid_registered_service
def get_duration(input_file: str):
    """Get video time duration

    :param input_file: input path
    :return: (duration in seconds, timedelta hour)
    :rtype: Union[float, datetime.timedelta]
    """

    ffprobe = FFProbe(input_file)
    duration = float(ffprobe.format().get("duration", 0))
    return duration, datetime.timedelta(duration)

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