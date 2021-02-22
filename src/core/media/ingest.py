import time

import csv, os
import ipfshttpclient

from src.core import Log, logger
from .download import ROOT_PATH, HOME_PATH
from .download import download_file

__author__ = 'gmena'

RECURSIVE_SLEEP_REQUEST = 10
IMAGE_INDEX = ["small_image", "medium_image", "large_image"]


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


def get_pb_domain_set(csv_file: str = 'pdm.csv') -> set:
    """
    Get public domain movies from csv
    :param csv_file: Path to csv file with pre-defined PDM movies list
    :return: Unique list of PDM
    """
    with open(f"{ROOT_PATH}/{csv_file}", 'r') as f:
        reader = csv.reader(f)
        return set([row[1] for row in reader])


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


def migrate_resource_hash(resources: dict, hash_: str) -> dict:
    """
    Re-struct resources adding the corresponding cid
    :param resources: ResourceScheme dict
    :param hash_: CID hash
    :return: ResourceScheme with CID assoc
    """
    for resource in resources:
        resource['cid'] = resource.get('cid', hash_)
    return resources


def migrate_image_hash(resources: dict, hash_: str) -> dict:
    """
    Re-struct image resources adding the corresponding cid
    :param resources: ImageScheme dict
    :param hash_: CID hash
    :return: ImageScheme with CID assoc
    """
    for x in IMAGE_INDEX:
        resources[x]['cid'] = resources[x].get('cid', hash_)
    return resources


def fetch_movie_resources(mv, current_imdb_code) -> dict:
    """
    Check if resources need to be downloaded and download it
    :param mv: ResourceSchema dict
    :param current_imdb_code: Imdb code key in collection
    :return: ResourceSchema dict
    """
    for resource in mv.get('resource'):
        if 'url' not in resource:
            continue
        resource['index'] = resource['index'] if 'index' in resource else 'index'
        resource_dir = '%s/%s/%s' % (current_imdb_code, resource['quality'], resource['index'])
        download_file(resource['url'], resource_dir)
    return mv


def fetch_images_resources(mv, current_imdb_code) -> dict:
    """
    Check if images need to be downloaded and download it
    :param mv: ImageSchema dict
    :param current_imdb_code: Imdb code key in collection
    :return: ImageScheme dict
    """
    for x in IMAGE_INDEX:
        if 'url' not in mv[x]:
            continue
        url = mv[x]['url']
        index = os.path.basename(url)
        download_file(mv[x]['url'], "%s/%s" % (current_imdb_code, index))
        mv[x]['index'] = mv[x]['index'] if 'index' in mv[x] else index
    return mv


def clean_resources(mv: dict) -> dict:
    """
    Clean url key from schema
    :param mv: Current movie meta processing
    :return: Cleaned schema
    """
    # Clean images url if defined
    for x in IMAGE_INDEX:
        if 'url' in mv[x]:
            del mv[x]['url']

    # Clean resource url if defined
    for resource in mv['resource']:
        if 'url' in resource:
            del resource['url']
    return mv


def ingest_ipfs_metadata(mv: dict) -> dict:
    """
    Loop over assets, download it and add it to IPFS
    :param mv: MovieSchema
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
        migrate_resource_hash(mv['resource'], hash_directory)
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
