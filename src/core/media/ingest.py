import os
import time
import errno
import ipfshttpclient

import src.core.helper as helper
from src.core import logger
from .process import resolve_root_dir

__author__ = 'gmena'

RECURSIVE_SLEEP_REQUEST = 10


def start_node():
    try:
        return ipfshttpclient.connect('/dns/ipfs/tcp/5001/http', session=True)
    except ipfshttpclient.exceptions.ConnectionError:
        logger.notice(f"Waiting for node active")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return start_node()


logger.notice(f"Starting node")
ipfs = start_node()  # Initialize api connection to node
logger.info(f"Node running {ipfs.id().get('ID')}")
logger.info('\n')


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
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT),
            directory
        )

    _hash = ipfs.add(directory, pin=True, recursive=True)
    _hash = map(lambda x: {'size': int(x['Size']), 'hash': x['Hash']}, _hash)
    _hash = max(_hash, key=lambda x: x['size'])['hash']
    logger.info(f"IPFS hash: {_hash}")
    return _hash


def ipfs_metadata(mv: dict) -> dict:
    """
    Loop over assets, download it and add it to IPFS
    :param mv: MovieScheme
    :return: Cleaned, pre-processed, structured ready schema
    """

    logger.warning(f"Ingesting {mv.get('imdb_code')}")
    # Logs on ready ingested
    current_dir = helper.util.build_dir(mv)
    hash_directory = ipfs_dir(current_dir)
    helper.util.sanitize_resource(mv['resource']['videos'], hash_directory)
    helper.util.sanitize_resource(mv['resource']['posters'].items(), hash_directory)

    mv['hash'] = hash_directory  # Add current hash to movie
    logger.success(f"Done {mv.get('imdb_code')}\n")
    return mv
