import nucleus.sdk.processing as processing
from nucleus.core.types import Path
from nucleus.sdk.harvest import Video
from nucleus.sdk.processing import HLS, VP9, Bitrate, Screen


def test_video_configuration(mock_local_video_path: Path):
    """Should compile the expected configuration"""
    video = Video(path=mock_local_video_path)
    video_engine = processing.engine(video)
    video_engine.configure(HLS(VP9()))
    video_engine.configure(Screen.Q1080)
    video_engine.configure(Bitrate.B1080)

    # check if compiled args are equal to expected
    compiled = sorted(video_engine.compile(), key=lambda t: t[0])
    assert compiled == [
        ('BR', {'b:v': '4096k', 'b:a': '320k'}),
        ('FrameSize', {'s': '1920x1080'}),
        (
            'HLS',
            {
                'hls_time': 10,
                'hls_list_size': 0,
                'hls_playlist_type': 'vod',
                'tag:v': 'hvc1',
                'c:a': 'aac',
                'c:v': 'libvpx-vp9',
            },
        ),
    ]
