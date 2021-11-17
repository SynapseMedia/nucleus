import os
import time
import errno
import ipfshttpclient
from typing import Iterator
from .. import util, logger
from src.sdk.web3.storage import pin_remote
from ..constants import TIMEOUT_REQUEST, RECURSIVE_SLEEP_REQUEST
from ..scheme.definition.movies import (
    MovieScheme,
    VideoScheme,
    PostersScheme,
    MultiMediaScheme,
)

__author__ = "gmena"

ipfs = None


def start_node():
    try:
        logger.log.notice("Starting node")
        ipfs_node = ipfshttpclient.connect(
            "/dns/ipfs/tcp/5001/http", session=True, timeout=TIMEOUT_REQUEST
        )
        logger.log.info(f"Node running {ipfs_node.id().get('ID')}")
        logger.log.info("\n")
        return ipfs_node
    except ipfshttpclient.exceptions.ConnectionError:
        logger.log.notice("Waiting for node active")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return start_node()


if __name__ == "__main__":
    ipfs = start_node()  # Initialize api connection to node


def add_dir_to_ipfs(_dir: str) -> str:
    """
    Go and conquer the world little child!!:
    Add directory to ipfs
    :param _dir: Directory to add to IPFS
    :return: The resulting CID
    """
    directory, path_exists = util.resolve_root_for(_dir)
    logger.log.notice(f"Ingesting directory: {directory}")

    if not path_exists:  # Check if path exist if not just
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), directory)

    _hash = ipfs.add(
        directory, recursive=True, cid_version=1, hash_function="blake2b-208"
    )

    _hash = map(lambda x: {"size": int(x["Size"]), "hash": x["Hash"]}, _hash)
    _hash = max(_hash, key=lambda x: x["size"])["hash"]
    logger.log.info(f"IPFS hash: {_hash}")
    return _hash


def _add_cid_to_posters(posters: PostersScheme, _hash: str) -> PostersScheme:
    """
    Replace route => cid declared in scheme PosterScheme
    :param posters:
    :param _hash:
    :return: PostersScheme
    """

    for key, poster in posters.iterable():
        file_format = util.extract_extension(poster.route)
        poster.route = _hash  # Overwrite older route
        poster.index = f"{key}.{file_format}"  # set new cid hash
    return posters


def _add_cid_to_videos(
    videos: Iterator[VideoScheme], _hash: str
) -> Iterator[VideoScheme]:
    """
    Replace route => cid declared in scheme VideoScheme
    :param videos:
    :param _hash:
    :return: VideoScheme
    """

    def _run(video: VideoScheme):
        video.route = _hash
        return video

    return map(_run, videos)


def _add_cid_to_resources(resource: MultiMediaScheme, _hash: str) -> MultiMediaScheme:
    """
    Re-struct resources adding the corresponding cid
    :param resource: MultimediaScheme
    :param _hash
    :return:
    """

    resource.posters = _add_cid_to_posters(resource.posters, _hash)
    resource.videos = _add_cid_to_videos(resource.videos, _hash)
    return resource


def pin_cid_list_remote(cid_list: iter) -> list:
    """
    Pin CID into IPFS remote node from list
    :param cid_list: List of cids to pin
    :return: cid list after pin
    """
    for cid in cid_list:
        logger.log.notice(f"Pinning cid to remote edge: {cid}")
        pin_remote(cid)
    return cid_list


def pin_cid_list(cid_list: iter) -> list:
    """
    Pin CID into IPFS node from list
    :param cid_list: List of cids to pin
    :return: cid list after pin
    """
    for cid in cid_list:
        logger.log.notice(f"Pinning cid: {cid}")
        ipfs.pin.add(cid)
    return cid_list


def to_ipfs_from(mv: MovieScheme) -> MovieScheme:
    """
    Loop over assets, download it and add it to IPFS
    :param mv: MovieScheme
    :return: Cleaned, pre-processed, structured ready MovieScheme
    """

    logger.log.warning(f"Ingesting {mv.imdb_code}")
    # Logs on ready ingested
    current_dir = util.build_dir(mv)
    hash_directory = add_dir_to_ipfs(current_dir)
    # Set hash by reference into posters and videos collections
    _add_cid_to_resources(mv.resource, hash_directory)

    # Add current hash to movie
    mv.hash = hash_directory
    logger.log.success(f"Done {mv.imdb_code}\n")
    return MovieScheme().dump(mv)
