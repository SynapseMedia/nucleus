import time
import ipfshttpclient

from src.core import Log, logger
from .download import resolve_root_dir
from .fetch import video_resources, image_resources
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
    directory = resolve_root_dir(_dir)
    logger.info(f"Ingesting directory: {Log.BOLD}{directory}{Log.ENDC}")
    _hash = ipfs.add(directory, pin=True, recursive=True)
    _hash = map(lambda x: {'size': int(x['Size']), 'hash': x['Hash']}, _hash)
    _hash = max(_hash, key=lambda x: x['size'])['hash']
    logger.info(f"IPFS hash: {Log.BOLD}{_hash}{Log.ENDC}")
    return _hash


def ipfs_file(_dir: str) -> str:
    """
    Go and conquer the world little child!!
    Add file to ipfs
    :param _dir: The tmp dir to store it
    :return: The resulting CID for file
    """
    logger.info(f"Ingesting file: {Log.BOLD}{_dir}{Log.ENDC}")
    _hash = ipfs.add(_dir, pin=True)['Hash']
    logger.info(f"IPFS hash: {Log.BOLD}{_hash}{Log.ENDC}")
    return _hash


def ipfs_metadata(mv: dict, max_retry=3) -> dict:
    """
    Loop over assets, download it and add it to IPFS
    :param mv: MovieScheme
    :param max_retry: Max retries on fail before raise exception
    :return: Cleaned, pre-processed, structured ready schema
    """
    try:
        logger.info(f"{Log.OKBLUE}Ingesting {mv.get('imdb_code')}{Log.ENDC}")
        # Downloading files
        current_imdb_code = mv.get('imdb_code')
        current_linked_name = mv.get('group_name', None)
        current_dir = current_imdb_code
        if current_linked_name:  # If linked_name add sub-dir
            current_dir = f"{current_linked_name}/{current_imdb_code}"

        # Fetch resources if needed
        mv = image_resources(mv, current_dir)
        mv = video_resources(mv, current_dir)

        # Logs on ready ingested
        hash_directory = ipfs_dir(current_dir)  # TODO not ingest yet, until transcode
        clean_resource_hash(mv, hash_directory)
        clean_image_hash(mv, hash_directory)

        mv['hash'] = hash_directory  # Add current hash to movie
        logger.info(f"{Log.OKGREEN}Done {mv.get('imdb_code')}{Log.ENDC}")
        logger.info('\n')
        return clean_resources(mv)
    except Exception as e:
        if max_retry <= 0:
            raise OverflowError('Max retry exceeded')
        max_retry = max_retry - 1
        logger.info(e)
        logger.error(f"Retry download assets error: {e}")
        logger.warning(f"{Log.WARNING}Wait {RECURSIVE_SLEEP_REQUEST}{Log.ENDC}")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return ipfs_metadata(mv, max_retry)
