from dataclasses import dataclass

from nucleus.core.types import Any, Mapping

"""
Aspect Ratio     H.264/AVC kb/s     Frame Rate
416 x 234       145                 ≤ 30 fps
640 x 360       365                 ≤ 30 fps
768 x 432       730, 1100           ≤ 30 fps
960 x 540       2000                same as source
1280 x 720      3000, 4500          same as source
1920 x 1080     6000, 7000          same as source
2560 x 1440     6000, 7000          same as source
"""

"""All these settings are defined by the ffmpeg library.
Reference: https://ffmpeg.org/ffmpeg.html#Main-options
"""


@dataclass(slots=True)
class Custom:
    """Special class for directly specifying custom settings to the ffmpeg command.

    Usage:

        # create a custom command based on ffmpeg option -fs
        # No further chunk of bytes is written after the limit is exceeded.
        custom = Custom(fs=100)
    """

    _custom: Mapping[str, Any]

    def __init__(self, **kwargs: Any):
        self._custom = kwargs

    def __iter__(self):
        yield from self._custom.items()


@dataclass(slots=True)
class FrameSize:
    """Set the frame size.

    Usage:

        # the output screen size
        size = FrameSize(200, 200)
    """

    width: int
    height: int

    def __str__(self) -> str:
        return f'{self.width}x{self.height}'

    def __iter__(self):
        yield 's', str(self)


@dataclass(slots=True)
class FPS:
    """Set the frame rate (Hz value, fraction or abbreviation).

    Usage:

        # frame per seconds
        fps = FPS(fs=60)
    """

    fps: float

    def __iter__(self):
        yield 'r', self.fps


@dataclass(slots=True)
class BR:
    """Set the Video/Audio bitrate.

    Usage:

        # set bitrate for both streams or independent
        br = BR(100) # audio/video
        br = BR(150, 94) # video b:v 150, audio b:a 94

    """

    video: int
    audio: int = 0

    def __iter__(self):
        # if we only receive video bitrate, we consider it as overall bitrate
        if self.video and not self.audio:
            yield 'b', f'{self.video}k'
            return

        yield 'b:v', f'{self.video}k'
        yield 'b:a', f'{self.audio}k'


@dataclass(frozen=True)
class Bitrate:
    """Default standard bitrate settings.

    Usage:

        # using default standard bitrate
        br = Bitrate.B720 # appropriate bitrate for 720p
    """

    B240 = BR(150, 94)
    B360 = BR(276, 128)
    B480 = BR(750, 192)
    B720 = BR(2048, 320)
    B1080 = BR(4096, 320)
    B2k = BR(6144, 320)
    B4k = BR(17408, 320)


@dataclass(frozen=True)
class Screen:
    """Default standard screen size settings.

    Usage:

        # using default screen sizes
        br = Screen.Q720 # appropriate size 720p

    """

    Q240 = FrameSize(416, 234)
    Q360 = FrameSize(640, 360)
    Q480 = FrameSize(854, 480)
    Q720 = FrameSize(1280, 720)
    Q1080 = FrameSize(1920, 1080)
    Q2k = FrameSize(2560, 1440)
    Q4k = FrameSize(3840, 2160)


__all__ = ('FPS', 'FrameSize', 'Screen', 'Bitrate', 'BR', 'Custom')
