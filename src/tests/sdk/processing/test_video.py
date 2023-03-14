import src.sdk.processing as processing

from src.core.types import Path
from src.sdk.harvest import Video
from src.sdk.processing import Screen, Bitrate, HLS, VP9


def test_video_configuration(mock_local_video_path: Path):
    """Should output the expected FFMPEG command using configured options"""
    output = Path("video.mp4")
    video = Video(route=mock_local_video_path)
    video_engine = processing.engine(video)
    video_engine.configure(HLS(VP9()))
    video_engine.configure(Screen.Q1080)
    video_engine.configure(Bitrate.B1080)

    command = video_engine.spec(output).compile()
    assert command == [
        "ffmpeg",
        "-i",
        "src/tests/_mock/files/video.mp4",
        "-b:a",
        "320k",
        "-b:v",
        "4096k",
        "-c:a",
        "aac",
        "-c:v",
        "libvpx-vp9",
        "-hls_list_size",
        "0",
        "-hls_playlist_type",
        "vod",
        "-hls_time",
        "10",
        "-s",
        "1920x1080",
        "-tag:v",
        "hvc1",
        "video.mp4",
    ]


# TODO comprobar aca si el formato existe en el origen FFProbe para HLS y DASH verificar primero
# TODO el codec que tiene el original si no es diferente al de salida solo copiar

