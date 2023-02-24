import src.sdk.processing.stream as stream

from src.core.types import Path
from src.sdk.processing.stream import Resolution, Screen, FPS


def test_hls_protocol(mock_local_video_path: Path):
    """Should be valid HLS setup"""
    custom_settings = {"-vcodec": "libx265"}
    stream_input = stream.input(mock_local_video_path, **custom_settings)
    streaming = stream_input.hls()
    assert streaming._params == {  # type: ignore
        "-video_source": mock_local_video_path,
        "-vcodec": "libx265",
    }
    assert streaming._protocol == "hls"  # type: ignore


def test_dash_protocol(mock_local_video_path: Path):
    """Should be valid DASH setup"""

    stream_input = stream.input(mock_local_video_path)
    streaming = stream_input.dash()
    assert streaming._params == {  # type: ignore
        "-video_source": mock_local_video_path
    }  # type: ignore
    assert streaming._protocol == "dash"  # type: ignore


def test_protocol_quality(mock_local_video_path: Path):
    """Should contains valid streams based on Quality options"""

    custom_settings = {"-vcodec": "libvpx-vp9", "-c:a": "copy"}
    stream_input = stream.input(mock_local_video_path, **custom_settings)
    protocol = stream_input.dash()

    quality_a = Resolution(Screen.Q1080, FPS.F60)
    quality_c = Resolution(Screen.Q720, FPS.F60)
    quality_list = [quality_a, quality_c]
    protocol.set_resolutions(quality_list)

    assert protocol._params == {  # type: ignore
        "-video_source": mock_local_video_path,
        "-c:a": "copy",
        "-vcodec": "libvpx-vp9",
        "-streams": [quality_a.dict(), quality_c.dict()],
    }
    assert protocol._protocol == "dash"  # type: ignore
