def to_dash(input_file: str, output_dir: str):
    """Transcode movie file to DASH and store file in output directory

    Facade function to transcode movie file to DASH

    :param input_file: Current file path
    :param output_dir: New file path
    :return: new file format dir
    :rtype: str
    """
    video = input(input_file, max_muxing_queue_size=MAX_MUXING_QUEUE_SIZE)
    quality = get_new_video_quality(input_file)
    current_format = util.extract_extension(input_file)
    logger.log.warn(f"Transcoding {current_format} to DASH using VP8 codec")

    dash = video.dash(Formats.vp8())
    dash.representations(*get_representations(quality))
    dash.output(output_dir, monitor=progress)
    sys.stdout.write("\n")
    return output_dir


def to_hls(input_file: str, output_dir: str):
    """Transcode movie file to HLS and store file in output directory

    Facade function to transcode movie file to HLS

    :param input_file: Current file path
    :param output_dir: New file path
    :return: new file format dir
    :rtype: str
    """
    video = input(input_file, max_muxing_queue_size=MAX_MUXING_QUEUE_SIZE)
    quality = get_new_video_quality(input_file)
    current_format = util.extract_extension(input_file)
    logger.log.warn(f"Transcoding {current_format} to HLS using H264 codec")

    hls = video.hls(Formats.h264(), hls_time=HLS_TIME)
    hls.representations(*get_representations(quality))
    hls.output(output_dir, monitor=progress)
    sys.stdout.write("\n")
    return output_dir
