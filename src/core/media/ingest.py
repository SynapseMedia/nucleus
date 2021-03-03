import time

import csv
import ipfshttpclient

from src.core import Log, logger
from .download import download_file, HOME_PATH
from .fetch import fetch_movie_resources, fetch_images_resources
from .clean import clean_resources, migrate_resource_hash, migrate_image_hash

__author__ = 'gmena'

RECURSIVE_SLEEP_REQUEST = 10


def start_node():
    try:
        return ipfshttpclient.connect('/dns/ipfs/tcp/5001/http', session=True)
    except ipfshttpclient.exceptions.ConnectionError:
        logger.info(f"{Log.WARNING}Waiting for node active{Log.ENDC}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return start_node()


logger.info(f"{Log.OKGREEN}Starting node{Log.ENDC}")
ipfs = start_node()  # Initialize api connection to node
logger.info(f"{Log.OKGREEN}Node running {ipfs.id().get('ID')}{Log.ENDC}")
logger.info('\n')


def ingest_ipfs_dir(_dir: str) -> str:
    """
    Go and conquer the world little child!!:
    Add directory to ipfs
    :param _dir: Directory to add to IPFS
    :return: The resulting CID
    """
    directory = "%s/torrents/%s" % (HOME_PATH, _dir)
    logger.info(f"Ingesting directory: {Log.BOLD}{_dir}{Log.ENDC}")
    _hash = ipfs.add(directory, pin=True, recursive=True)
    _hash = next(item for item in _hash if item['Name'] == _dir)['Hash']
    logger.info(f"IPFS hash: {Log.BOLD}{_hash}{Log.ENDC}")
    return _hash


def ingest_ipfs_file(uri: str, _dir: str) -> str:
    """
    Go and conquer the world little child!!
    Add file to ipfs
    :param uri: The link to file
    :param _dir: The tmp dir to store it
    :return: The resulting CID for file
    """
    directory = download_file(uri, _dir)
    logger.info(f"Ingesting file: {Log.BOLD}{_dir}{Log.ENDC}")
    _hash = ipfs.add(directory, pin=True)['Hash']
    logger.info(f"IPFS hash: {Log.BOLD}{_hash}{Log.ENDC}")
    return _hash


def ingest_ipfs_metadata(mv: dict) -> dict:
    """
    Loop over assets, download it and add it to IPFS
    :param mv: MovieScheme
    :return: Cleaned, pre-processed, structured ready schema
    """
    try:
        logger.info(f"{Log.OKBLUE}Ingesting {mv.get('imdb_code')}{Log.ENDC}")
        # Downloading files
        current_imdb_code = mv.get('imdb_code')

        # Fetch resources if needed
        mv = fetch_images_resources(mv, current_imdb_code)
        mv = fetch_movie_resources(mv, current_imdb_code)

        # Logs on ready ingested
        hash_directory = ingest_ipfs_dir(current_imdb_code)
        migrate_resource_hash(mv, hash_directory)
        migrate_image_hash(mv, hash_directory)

        mv['hash'] = hash_directory  # Add current hash to movie
        logger.info(f"{Log.OKGREEN}Done {mv.get('imdb_code')}{Log.ENDC}")
        logger.info('\n')
        return clean_resources(mv)
    except Exception as e:
        logger.error(f"Retry download assets error: {e}")
        logger.warning(f"{Log.WARNING}Wait {RECURSIVE_SLEEP_REQUEST}{Log.ENDC}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return ingest_ipfs_metadata(mv)
