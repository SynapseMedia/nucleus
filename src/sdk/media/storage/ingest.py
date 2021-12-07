import os
import errno

from .remote import pin_remote
from src.sdk import util, logger
from src.sdk.media.storage import ipfs
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

    _hash = ipfs.add(
        directory, recursive=True, cid_version=1, hash_function="blake2b-208"
    )

    _hash = map(lambda x: {"size": int(x["Size"]), "hash": x["Hash"]}, _hash)
    _hash = max(_hash, key=lambda x: x["size"])["hash"]
    logger.log.info(f"IPFS hash: {_hash}")
    return _hash


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
