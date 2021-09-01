import ffmpeg
from src.core import logger
from src.core import helper

DEFAULT_FORMAT = "hls"
DEFAULT_HLS_TIME = 5
DEFAULT_HLS_FORMAT = "m3u8"
DEFAULT_NEW_FILENAME = "index.m3u8"


def to_hls(input_file, output_dir):
    """
    Transcode movie file to hls
    :param input_file:
    :param output_dir
    :return: new file format dir
    """

    probe = ffmpeg.probe(input_file)
    total_duration = float(probe["format"]["duration"])
    show_progress = helper.transcode.show_progress(total_duration)
    video_stream = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
        None,
    )

    # When transcoding audio and/or video streams, ffmpeg will not begin writing into the output until it has one
    # packet for each such stream. While waiting for that to happen, packets for other streams are buffered.
    # This option sets the size of this buffer, in packets, for the matching
    # output stream.
    output_args = {"max_muxing_queue_size": 9999}
    if video_stream["codec_name"] == "h264":
        output_args["vcodec"] = "copy"
        logger.success("vcodec copy mode: enabled")

    with show_progress as socket_filename:
        try:
            (
                ffmpeg.input(input_file)
                .output(
                    output_dir,
                    format=DEFAULT_FORMAT,
                    start_number=0,
                    hls_time=DEFAULT_HLS_TIME,
                    hls_list_size=0,
                    **output_args,
                )
                .global_args("-progress", "unix://{}".format(socket_filename))
                .run(
                    overwrite_output=True,
                    capture_stdout=True,
                    capture_stderr=True,
                )
            )
        except ffmpeg.Error as e:
            print(e.stderr)
            logger.error(f"Error transcoding {input_file}")

    return output_dir
