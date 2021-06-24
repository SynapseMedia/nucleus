import ffmpeg
from src.core import logger
from src.core import helper
from .process import make_destination_dir, PROD_PATH, RAW_PATH

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
    output_dir = file_dir.replace(file_format, DEFAULT_HLS_FORMAT)
    output_dir = output_dir.replace(RAW_PATH, PROD_PATH)
    make_destination_dir(output_dir)

    if file_format == DEFAULT_HLS_FORMAT:  # transcode hls from hls?
        logger.warning(f"Invalid source format {file_format}")

    stream = ffmpeg.input(file_dir, f=file_format)
    stream = ffmpeg.output(
        stream, output_dir,
        format=DEFAULT_FORMAT, start_number=0,
        hls_time=DEFAULT_HLS_TIME, hls_list_size=0
    )

    ffmpeg.run(stream, overwrite_output=True)
    return output_dir
