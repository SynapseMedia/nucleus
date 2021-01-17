import time

import csv
import ipfshttpclient

from resource.py import Log
from .download import ROOT_PATH
from .download import download_file

__author__ = 'gmena'

RECURSIVE_SLEEP_REQUEST = 10

try:
    ipfs = ipfshttpclient.connect('/dns/ipfs/tcp/5001/http', session=True)
    print(ipfs.id())
except ipfshttpclient.exceptions.ConnectionError:
    pass


def get_pb_domain_set(csv_file='pdm.csv'):
    """
    Get public domain movies from csv
    :param csv_file:
    :return:
    """
    with open(f"{ROOT_PATH}/{csv_file}", 'r') as f:
        reader = csv.reader(f)
        return set([row[1] for row in reader])


def ingest_ipfs_dir(_dir):
    """
    Go and conquer the world little child!!:
    Add directory to ipfs
    :param _dir:
    :return:
    """
    directory = "%s/torrents/%s" % (ROOT_PATH, _dir)
    print(f"Ingesting directory: {Log.BOLD}{_dir}{Log.ENDC}")
    _hash = ipfs.add(directory, pin=True, recursive=True)
    _hash = next(item for item in _hash if item['Name'] == _dir)['Hash']
    print(f"IPFS hash: {Log.BOLD}{_hash}{Log.ENDC}")
    return _hash


def ingest_ipfs_file(uri, _dir):
    """
    Go and conquer the world little child!!
    Add file to ipfs
    :param uri:
    :param _dir:
    :return:
    """
    directory = download_file(uri, _dir)
    print(f"Ingesting file: {Log.BOLD}{_dir}{Log.ENDC}")
    _hash = ipfs.add(directory, pin=True)['Hash']
    print(f"IPFS hash: {Log.BOLD}{_hash}{Log.ENDC}")
    return _hash


def ingest_ipfs_metadata(mv: list):
    """
    Loop over assets, download it and add it to IPFS
    Please check movies scheme in https://yts.mx/api
    :param mv: List of movies
    :return:
    """
    try:
        print(f"\n{Log.OKBLUE}Ingesting {mv['imdb_code']}{Log.ENDC}")
        # Downloading files
        current_imdb_code = mv['imdb_code']
        image_index = [  # Index image movie lists
            "background_image", "background_image_original",
            "small_cover_image", "medium_cover_image",
            "large_cover_image"
        ]

        for x in image_index:
            if x in mv:  # Download all image assets
                download_file(mv[x], "%s/%s.jpg" % (current_imdb_code, x))

        for torrent in mv['torrents']:
            torrent_dir = '%s/%s/%s' % (current_imdb_code, torrent['quality'], torrent['hash'])
            download_file(torrent['url'], torrent_dir)

        # Logs on ready ingested
        hash_directory = ingest_ipfs_dir(current_imdb_code)
        mv['hash'] = hash_directory
        print(f"{Log.OKGREEN}Done {mv['imdb_code']}{Log.ENDC}\n")
        return mv
    except Exception as e:
        print('Retry download assets error:', e)
        print("\n\033[93mWait", str(RECURSIVE_SLEEP_REQUEST), 'seconds\033[0m\n')
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return ingest_ipfs_metadata(mv)
