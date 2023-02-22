
import src.sdk.processing as processing

from src.core.types import Path
# from src.sdk.processing.stream import Quality, Sizes, FPS
from src.sdk.processing.transcode import InputNode


def test_video_engine(mock_local_file_path: Path):
    """Should be valid VideoEngine instance"""
    video_engine = processing.VideoEngine(mock_local_file_path)
    with video_engine as engine:
        assert isinstance(engine._input, InputNode)  # type: ignore

