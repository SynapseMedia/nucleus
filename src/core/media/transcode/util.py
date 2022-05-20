import datetime
from ffmpeg_streaming import FFProbe


def get_duration(input_file: str):
    """Get video time duration

    :param input_file: input path
    :return: (duration in seconds, timedelta hour)
    :rtype: Union[float, datetime.timedelta]
    """

    ffprobe = FFProbe(input_file)
    duration = float(ffprobe.format().get("duration", 0))
    return duration, datetime.timedelta(duration)
