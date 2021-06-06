import time
import ipfshttpclient

import src.core.helper as helper
from src.core import Log, logger
from .download import resolve_root_dir
from .clean import clean_resources, clean_resource_hash, clean_image_hash

__author__ = 'gmena'

RECURSIVE_SLEEP_REQUEST = 10


def start_node():
    try:
        return ipfshttpclient.connect('/dns/ipfs/tcp/5001/http', session=True)
    except ipfshttpclient.exceptions.ConnectionError:
        logger.info(f"{Log.WARNING}Waiting for node active{Log.ENDC}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return start_node()


if __name__ == '__main__':
    logger.info(f"{Log.OKGREEN}Starting node{Log.ENDC}")
    ipfs = start_node()  # Initialize api connection to node
    logger.info(f"{Log.OKGREEN}Node running {ipfs.id().get('ID')}{Log.ENDC}")
    logger.info('\n')


def ipfs_dir(_dir: str) -> str:
    """
    Go and conquer the world little child!!:
    Add directory to ipfs
    :param _dir: Directory to add to IPFS
    :return: The resulting CID
    """
    directory = resolve_root_dir(_dir, True)
    logger.info(f"Ingesting directory: {Log.BOLD}{directory}{Log.ENDC}")
    _hash = ipfs.add(directory, pin=True, recursive=True)
    _hash = map(lambda x: {'size': int(x['Size']), 'hash': x['Hash']}, _hash)
    _hash = max(_hash, key=lambda x: x['size'])['hash']
    logger.info(f"IPFS hash: {Log.BOLD}{_hash}{Log.ENDC}")
    return _hash


def ipfs_metadata(mv: dict) -> dict:
    """
    Loop over assets, download it and add it to IPFS
    :param mv: MovieScheme
    :return: Cleaned, pre-processed, structured ready schema
    """

    logger.info(f"{Log.OKBLUE}Ingesting {mv.get('imdb_code')}{Log.ENDC}")
    # Logs on ready ingested
    current_dir = helper.util.build_dir(mv)
    hash_directory = ipfs_dir(current_dir)
    clean_resource_hash(mv, hash_directory)
    clean_image_hash(mv, hash_directory)

    mv['hash'] = hash_directory  # Add current hash to movie
    logger.info(f"{Log.OKGREEN}Done {mv.get('imdb_code')}\n{Log.ENDC}")
    return clean_resources(mv)
