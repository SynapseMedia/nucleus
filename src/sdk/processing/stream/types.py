from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from vidgear.gears import StreamGear  # type: ignore


Stream = StreamGear


class Size:
    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"{self.width}x{self.height}"


class FPS(float, Enum):
    F30 = 30.0
    F60 = 60.0
    F120 = 120.0


class Resolution:

    """This class groups the properties required for standard video processing."""

    def __init__(self, size: Size, fps: FPS):
        self.size = size
        self.fps = fps

    def dict(self):
        """Return expected quality settings for StreamGear settings"""
        return {
            "-framerate": self.fps,
            "-resolution": str(self.size),
        }


@dataclass(frozen=True)
class Screen:
    Q144 = Size(256, 144)
    Q240 = Size(426, 240)
    Q360 = Size(640, 360)
    Q480 = Size(854, 480)
    Q720 = Size(1280, 720)
    Q1080 = Size(1920, 1080)
    Q2k = Size(2560, 1440)
    Q4k = Size(3840, 2160)
