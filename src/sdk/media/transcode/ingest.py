from ... import logger, util
from .codecs import to_hls, to_dash
from ...scheme.definition.movies import MediaScheme
from ...constants import HLS_FORMAT, DASH_FORMAT


def videos(video: MediaScheme, protocol: str, output_dir: str):
    """
    Transcode video listed in metadata
    :param video: VideoScheme
    :param protocol:
    :param output_dir: dir to store transcoding video
    :return:
    """

    protocols = {HLS_FORMAT: to_hls, DASH_FORMAT: to_dash}

    if protocol not in protocols:
        logger.log.error("Invalid protocol provided. Please try using `hls` or `dash`")
        return

    util.make_destination_dir(output_dir)
    protocols[protocol](video.route, output_dir)
    logger.log.success(f"New movie stored in: {output_dir} \n")
