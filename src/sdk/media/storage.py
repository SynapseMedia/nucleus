import os
import time
import errno
import ipfshttpclient
import requests
from ipfshttpclient.exceptions import ErrorResponse

from typing import Iterator
from .. import util, logger
from ..constants import (
    TIMEOUT_REQUEST,
    RECURSIVE_SLEEP_REQUEST,
    VALIDATE_SSL,
    PINATA_API_SECRET,
    PINATA_API_KEY,
    PINATA_ENDPOINT,
    PINATA_PSA,
    PINATA_SERVICE,
    PINATA_API_JWT,
    PINATA_PIN_BACKGROUND,
)
from ..scheme.definition.movies import (
    MovieScheme,
    VideoScheme,
    PostersScheme,
    MultiMediaScheme,
)

__author__ = "gmena"

ipfs = None
# Session keep alive
session = requests.Session()


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


def _find_service_in_list(service: dict):
    """
    Check if "pinata" is a pin remote service in node
    :param service: Current processed Service dic
    :return: Tuple with value found or tuple with None (None,) || (pinata,)
    """
    return next(
        (
            i["Service"]
            for i in service["RemoteServices"]
            if i["Service"] == PINATA_SERVICE
        ),
        None,
    )


def has_valid_registered_service():
    """
    Check if pinata service is already registered
    :return: False if not registered else True
    """
    ipfs_api_client = ipfs.get_client()
    args = (PINATA_SERVICE, PINATA_PSA, PINATA_API_JWT)
    registered_services = ipfs_api_client.request(
        "/pin/remote/service/ls", args, decoder="json"
    )

    # Map resulting from registered services and search for "pinata"
    find_registered_service = map(_find_service_in_list, registered_services)
    return PINATA_SERVICE in tuple(filter(None, find_registered_service))


def pin_remote(cid: str, **kwargs):
    """
    Pin cid into edge pinata remote cache
    :param cid: the cid to pin
    :return
    """

    if not has_valid_registered_service():
        register_service()

    try:
        args = (cid,)
        ipfs_api_client = ipfs.get_client()
        kwargs.setdefault(
            "opts", {"service": PINATA_SERVICE, "background": PINATA_PIN_BACKGROUND}
        )
        return ipfs_api_client.request(
            "/pin/remote/add", args, decoder="json", **kwargs
        )
    except ErrorResponse:
        logger.log.warning("Object already pinned to pinata")
        logger.log.warning("Please remove or replace existing pin object")
        logger.log.info("\n")


def register_service():
    """
    Register edge service in ipfs node
    :return: request result according to
    https://docs.ipfs.io/reference/http/api/#api-v0-pin-remote-service-add
    """
    if has_valid_registered_service():
        logger.log.warning("Service already registered")
        return

    ipfs_api_client = ipfs.get_client()
    args = (PINATA_SERVICE, PINATA_PSA, PINATA_API_JWT)
    logger.log.info("Registering pinata service")
    return ipfs_api_client.request("/pin/remote/service/add", args, decoder="json")


def check_status():
    """
    Ping request to check for valid auth
    for pinata service
    :return: True if active service else False
    """
    # Start http session
    response = session.get(
        f"{PINATA_ENDPOINT}/data/testAuthentication",
        verify=VALIDATE_SSL,
        headers={
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_API_SECRET,
        },
    )

    # Check status for response
    return response.status_code == requests.codes.ok and has_valid_registered_service()


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


def ingest_to_ipfs(mv: MovieScheme) -> MovieScheme:
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
