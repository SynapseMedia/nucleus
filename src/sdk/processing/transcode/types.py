from __future__ import annotations

from dataclasses import dataclass
from ffmpeg.nodes import FilterableStream  # type: ignore


class Size:
    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"{self.width}x{self.height}"


@dataclass(frozen=True)
class Screen:
    Q240 = Size(416, 234)
    Q360 = Size(640, 360)
    Q480 = Size(854, 480)
    Q720 = Size(1280, 720)
    Q1080 = Size(1920, 1080)
    Q2k = Size(2560, 1440)
    Q4k = Size(3840, 2160)


__all__ = ("FilterableStream",)
