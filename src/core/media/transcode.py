import ffmpeg, sys, os
from src.core import logger
from src.core import helper

DEFAULT_FORMAT = 'hls'
DEFAULT_HLS_TIME = 5
DEFAULT_HLS_FORMAT = 'm3u8'
DEFAULT_NEW_FILENAME = 'index.m3u8'


def to_hls(input_file, output_dir):
    """
    Transcode movie file to hls
    :param input_file:
    :param output_dir
    :return: new file format dir
    """
    filename = os.path.basename(input_file)
    file_format = helper.util.extract_extension(input_file)
    filename_cleaned = filename.replace(file_format, DEFAULT_HLS_FORMAT)
    output_dir = f"{output_dir}{filename_cleaned}"

    if file_format == DEFAULT_HLS_FORMAT:  # transcode hls from hls?
        logger.warning(f"Invalid source format {file_format}")
    probe = ffmpeg.probe(input_file)
    total_duration = float(probe['format']['duration'])
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    output_args = {}
    if video_stream['codec_name'] == 'h264':
        output_args['vcodec'] = 'copy'
        logger.info('vcodec copy mode enabled')
    with helper.transcoder.show_progress(total_duration) as socket_filename:
        try:
            (ffmpeg.input(input_file)
             .output(output_dir, format=DEFAULT_FORMAT, start_number=0, hls_time=DEFAULT_HLS_TIME, hls_list_size=0, **output_args)
             .global_args('-progress', 'unix://{}'.format(socket_filename))
             .run(overwrite_output=True, capture_stdout=True, capture_stderr=True))
        except ffmpeg.Error as e:
            logger.error(e.stderr)
            sys.exit(1)

    return output_dir
