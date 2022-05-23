from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod
from ffmpeg_streaming import Bitrate, Representation, Size, input, FFProbe


class Protocols(Enum):
    HLS = 0
    DASH = 1


class Quality(Enum):
    Q144 = 0
    Q240 = 1
    Q360 = 2
    Q480 = 3
    Q720 = 4
    Q1080 = 5
    Q2k = 6
    Q4k = 7


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


class Input:
    """Class to allow control over FFmpeg input.

    This class is designed to process one video file at a time
    """

    def __init__(self, input_file: str, **options):
        self.path = input_file
        self.media = input(input_file, **options)

    def get_path(self):
        return self.path

    def get_video_size(self):
        """Return video size

        :return: Video size from input file
        :rtype: Size
        """
        ffprobe = FFProbe(self.path)
        return ffprobe.video_size

    def get_duration(self):
        """Get video time duration

        :param input_file: input path
        :return: (duration in seconds, timedelta hour)
        :rtype: Union[float, datetime.timedelta]
        """

        ffprobe = FFProbe(self.path)
        duration = float(ffprobe.format().get("duration", 0))
        return duration, datetime.timedelta(duration)


class Codec(ABC):
    def __init__(self, input: Input):
        super().__init__()
        self.input = input

    @abstractmethod
    def set_input(self, input: Input):
        pass

    @abstractmethod
    def set_representation(self, repr: Representation):
        pass

    @property
    @abstractmethod
    def format():
        pass

    @abstractmethod
    def transcode(output_dir: str):
        pass
