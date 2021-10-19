import os
import time
import errno
import ipfshttpclient

from src.core import logger, util
from .fetch import resolve_root_dir
from .transcode import DEFAULT_NEW_FILENAME

__author__ = "gmena"

RECURSIVE_SLEEP_REQUEST = 10
TIMEOUT_REQUEST = 30 * 60


def start_node():
    try:
        return ipfshttpclient.connect(
            "/dns/ipfs/tcp/5001/http", session=True, timeout=TIMEOUT_REQUEST
        )
    except ipfshttpclient.exceptions.ConnectionError:
        logger.notice("Waiting for node active")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return start_node()


logger.notice("Starting node")
ipfs = start_node()  # Initialize api connection to node
logger.info(f"Node running {ipfs.id().get('ID')}")
logger.info("\n")


def ipfs_dir(_dir: str) -> str:
    """
    Go and conquer the world little child!!:
    Add directory to ipfs
    :param _dir: Directory to add to IPFS
    :return: The resulting CID
    """
    directory, path_exists = resolve_root_dir(_dir, True)
    logger.notice(f"Ingesting directory: {directory}")

    if not path_exists:  # Check if path exist if not just
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), directory)

    _hash = ipfs.add(directory, recursive=True)
    _hash = map(lambda x: {"size": int(x["Size"]), "hash": x["Hash"]}, _hash)
    _hash = max(_hash, key=lambda x: x["size"])["hash"]
    logger.info(f"IPFS hash: {_hash}")
    return _hash


def _add_cid_to_posters(posters, _hash):
    """
    Replace route => cid declared in scheme PosterScheme
    :param posters:
    :param _hash:
    :return:
    """
    for key, resource in posters.items():
        resource_origin = resource["route"]  # Input dir resource
        file_format = util.extract_extension(resource_origin)
        resource.update({"cid": _hash, "index": f"{key}.{file_format}"})
        del resource["route"]


def _add_cid_to_videos(videos, _hash):
    """
    Replace route => cid declared in scheme VideoScheme
    :param videos:
    :param _hash:
    :return:
    """
    for resource in videos:
        resource.update({"cid": _hash, "index": DEFAULT_NEW_FILENAME})
        del resource["route"]


def _add_cid_to_resource(mv: dict, _hash):
    """
    Re-struct resources adding the corresponding cid
    :param mv:
    :param _hash
    :return:
    """
    videos_resource = mv["resource"]["videos"]
    posters_resources = mv["resource"]["posters"]

    _add_cid_to_posters(posters_resources, _hash)
    _add_cid_to_videos(videos_resource, _hash)


def ipfs_pin_cid(cid_list):
    for cid in cid_list:
        logger.notice(f"Pinning cid: {cid}")
        ipfs.pin.add(cid)


def ipfs_metadata(mv: dict) -> dict:
    """
    Loop over assets, download it and add it to IPFS
    :param mv: MovieScheme
    :return: Cleaned, pre-processed, structured ready schema
    """

    logger.warning(f"Ingesting {mv.get('imdb_code')}")
    # Logs on ready ingested
    current_dir = util.build_dir(mv)
    hash_directory = ipfs_dir(current_dir)
    _add_cid_to_resource(mv, hash_directory)
    mv["hash"] = hash_directory  # Add current hash to movie
    logger.success(f"Done {mv.get('imdb_code')}\n")
    return mv
