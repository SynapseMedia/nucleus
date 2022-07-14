from src.core import json, logger
from src.core.storage.ipfs import pin, add_dir
from .edge import pin as remote_pin
from ..scheme.definition.movies import MovieScheme

__author__ = "gmena"


def to_ipfs(mv: MovieScheme):
    """Ingest movie to IPFS

    :param mv: MovieScheme
    :return: Cleaned, pre-processed, structured ready MovieScheme
    """

    logger.log.warning(f"Ingesting {mv.imdb_code}")
    # Logs on ready ingested
    current_dir = json.build_dir(mv)
    return add_dir(current_dir)


def pin_cid(cid_list: iter, remote: bool):
    """Pin CID into Local/Remote node from list

    :param cid_list: List of cid to pin
    :param remote: Pin in remote edge node if true
    :return: cid list after pin
    """
    for cid in cid_list:
        logger.log.notice(f"Pinning cid: {cid}")
        pin(cid) if not remote else remote_pin(cid)
    return cid_list
