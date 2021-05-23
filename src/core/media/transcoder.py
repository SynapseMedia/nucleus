import ffmpeg
from src.core import helper

DEFAULT_FORMAT = 'hls'
DEFAULT_HLS_TIME = 5
DEFAULT_HLS_FORMAT = '.m3u8'


def to_hls(file_dir):
    """
    Transcode movie file to hls
    :param file_dir:
    :return: new file format dir
    """
    file_format = helper.transcoder.extract_extension(file_dir)
    new_format = file_dir.replace(file_dir, file_format)

    input_stream = ffmpeg.input(file_dir, f=file_format)
    output_stream = ffmpeg.output(
        input_stream, new_format,
        format=DEFAULT_FORMAT, start_number=0,
        hls_time=DEFAULT_HLS_TIME, hls_list_size=0
    )

    ffmpeg.run(output_stream)
    return output_stream
