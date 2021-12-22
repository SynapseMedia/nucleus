import os
import errno

from src.sdk import util, logger
from .remote import pin as remote_pin
from src.sdk.media.storage.ipfs import exec_command
from src.sdk.scheme.definition.movies import MovieScheme

__author__ = "gmena"


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

    # avoid pin by default /reference/http/api/#http-commands
    # hash needed to encode to bytes16 and hex
    args = (
        directory,
        "--recursive",
        "--quieter",
        "--cid-version=1",
        "--pin=false",
        "--hash=blake2b-208",
    )

    _hash = exec_command("add", *args)
    logger.log.info(f"IPFS hash: {_hash.strip()}")
    return _hash.strip()


def pin(cid):
    """
    Pin cid into local node
    :param cid: the cid to pin
    :return
    """

    return exec_command("/pin/add/", cid)


def pin_cid_list(cid_list: iter, remote: bool) -> list:
    """
    Pin CID into Local/Remote node from list
    :param cid_list: List of cid to pin
    :param remote: Pin in remote edge node if true
    :return: cid list after pin
    """
    for cid in cid_list:
        logger.log.notice(f"Pinning cid: {cid}")
        pin(cid) if not remote else remote_pin(cid)
    return cid_list


def dag_get(cid):
    """
    Retrieve dag information from cid
    :param cid:
    """
    return exec_command("/dag/get", cid)


def to_ipfs(mv: MovieScheme) -> str:
    """
    Loop over assets, download it and add it to IPFS
    :param mv: MovieScheme
    :return: Cleaned, pre-processed, structured ready MovieScheme
    """

    logger.log.warning(f"Ingesting {mv.imdb_code}")
    # Logs on ready ingested
    current_dir = util.build_dir(mv)
    return add_dir_to_ipfs(current_dir)
