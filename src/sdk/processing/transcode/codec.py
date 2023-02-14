from src.core.types import Any, Directory
from .types import Streaming
from .ffmpeg import input
from .protocols import DASH, HLS

# TODO test these functions

def to_dash(input_file: Directory, **options: Any) -> Streaming:
    with input(input_file, **options) as _input:
        return DASH(_input)


def to_hls(input_file: Directory, **options: Any) -> Streaming:
    with input(input_file, **options) as _input:
        return HLS(_input)
