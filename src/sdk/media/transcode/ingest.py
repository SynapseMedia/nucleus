from src.core.media.transcode.codecs import get_codec
from src.core.exception import InvalidCodec
from src.core import logger, util


def videos(video_path: str, protocol: str, output_dir: str):
    """Transcode video listed in metadata and store transcoded file in output directory

    :param video_path: Video input file path
    :param protocol: HLS_FORMAT | DASH_FORMAT
    :param output_dir: dir where to store the transcoded video
    :return:
    """

    codec = get_codec(protocol)

    if not codec:
        raise InvalidCodec("Protocol %s in not supported" % protocol)

    # Build output path
    util.make_destination_dir(output_dir)
    # Execute codec function to transcode video from path
    protocol(video_path, output_dir)
    logger.log.success(f"New movie stored in: {output_dir} \n")
