import ffmpeg, os, sys
from src.core import logger
from src.core import helper

DEFAULT_FORMAT = 'hls'
DEFAULT_HLS_TIME = 5
DEFAULT_HLS_FORMAT = 'm3u8'


def to_hls(input_file, output_dir):
    """
    Transcode movie file to hls
    :param input_file:
    :param output_dir
    :return: new file format dir
    """
    filename = os.path.basename(input_file)
    file_format = helper.transcoder.extract_extension(input_file)
    filename_cleaned = filename.replace(file_format, DEFAULT_HLS_FORMAT)
    output_dir = f"{output_dir}{filename_cleaned}"

    if file_format == DEFAULT_HLS_FORMAT:  # transcode hls from hls?
        logger.warning(f"Invalid source format {file_format}")

    total_duration = float(ffmpeg.probe(input_file)['format']['duration'])
    with helper.transcoder.show_progress(total_duration) as socket_filename:
        try:
            (ffmpeg.input(input_file)
             .output(output_dir, format=DEFAULT_FORMAT, start_number=0, hls_time=DEFAULT_HLS_TIME, hls_list_size=0)
             .global_args('-progress', 'unix://{}'.format(socket_filename))
             .run(overwrite_output=True, capture_stdout=True, capture_stderr=True))
        except ffmpeg.Error as e:
            logger.error(e.stderr)
            sys.exit(1)

    return output_dir
