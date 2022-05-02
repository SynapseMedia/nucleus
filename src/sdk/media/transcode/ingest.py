from ... import logger, util
from .codecs import to_hls, to_dash
from ...constants import HLS_FORMAT, DASH_FORMAT


def videos(video_path: str, protocol: str, output_dir: str):
    """Transcode video listed in metadata and store transcoded file in output directory

    :param video_path: Video input file path
    :param protocol: HLS_FORMAT | DASH_FORMAT
    :param output_dir: dir where to store the transcoded video
    :return:
    """

    protocols = {HLS_FORMAT: to_hls, DASH_FORMAT: to_dash}

    if protocol not in protocols:
        logger.log.error("Invalid protocol provided. Please try using `hls` or `dash`")
        return

    util.make_destination_dir(output_dir)
    protocols[protocol](video_path, output_dir)
    logger.log.success(f"New movie stored in: {output_dir} \n")
