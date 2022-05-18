import os
import errno

from src.sdk import util, logger
from .edge import pin as remote_pin
from src.sdk.media.storage.ipfs import exec_command, pin
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

    if not path_exists:  # Check if path exist if not just pin_cid_list
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


def pin_cid(cid_list: iter, remote: bool) -> list:
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


def to_ipfs(mv: MovieScheme):
    """Ingest movie to IPFS

    :param mv: MovieScheme
    :return: Cleaned, pre-processed, structured ready MovieScheme
    """

    logger.log.warning(f"Ingesting {mv.imdb_code}")
    # Logs on ready ingested
    current_dir = util.build_dir(mv)
    return add_dir_to_ipfs(current_dir)
