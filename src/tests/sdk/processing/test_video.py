import src.sdk.processing as processing

from src.core.types import Path
from src.sdk.harvest import Video
from src.sdk.processing import Screen, Bitrate, HLS, VP9


def test_video_configuration(mock_local_video_path: Path):
    """Should compile the expected configuration"""
    video = Video(route=mock_local_video_path)
    video_engine = processing.engine(video)
    video_engine.configure(HLS(VP9()))
    video_engine.configure(Screen.Q1080)
    video_engine.configure(Bitrate.B1080)

    # check if compiled args are equal to expected
    compiled = sorted(video_engine.compile(), key=lambda t: t[0])
    assert compiled == [
        ("BR", {"b:v": "4096k", "b:a": "320k"}),
        (
            "HLS",
            {
                "hls_time": 10,
                "hls_list_size": 0,
                "hls_playlist_type": "vod",
                "tag:v": "hvc1",
                "c:a": "aac",
                "c:v": "libvpx-vp9",
            },
        ),
        ("Size", {"s": "1920x1080"}),
    ]
