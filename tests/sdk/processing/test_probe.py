import pytest

import nucleus.sdk.processing as processing
from nucleus.core.types import Path
from nucleus.sdk.harvest import Video
from nucleus.sdk.processing import H264, HLS, Copy

# TODO add mocking


@pytest.mark.skip(reason='no way of currently testing this. mock needed')
def test_probe_video(mock_local_video_path: Path):
    """Integration test example to check the video codec using probe"""

    # lets get the summary of input video
    probe = processing.probe(mock_local_video_path)
    input_codec = probe['streams'][0].codec_name

    video = Video(path=mock_local_video_path)
    video_engine = processing.engine(video)
    output_codec = Copy('v')  # by default copy the source video codec to avoid overhead re-encoding

    # encode the source video h264 only if not the same of resource
    if input_codec not in H264():
        output_codec = H264()

    video_engine.configure(HLS(output_codec))
    # then let see if the video match the output codec
    assert input_codec in H264()
