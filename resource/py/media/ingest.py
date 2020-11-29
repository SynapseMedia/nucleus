import csv
import ipfshttpclient
import os
import random
import re
import requests
from multiprocessing import Pool
from pathlib import Path

from resource.py import Log

__author__ = 'gmena'
# Session keep alive
# http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects

root_path = os.path.dirname(os.path.realpath(__file__))
_agents = [
    'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
]

try:
    ipfs = ipfshttpclient.connect('/dns/ipfs/tcp/5001/http')
    print(ipfs.id())
except ipfshttpclient.exceptions.ConnectionError:
    pass


def get_pb_domain_set(csv_file='pdm.csv'):
    with open(f"{root_path}/{csv_file}", 'r') as f:
        reader = csv.reader(f)
        return set([row[1] for row in reader])


def download_file(uri, _dir):
    """
    Take from the boring centralized network
    :param uri:
    :param _dir:
    :return:
    """
    session = requests.Session()
    directory = "%s/torrents/%s" % (root_path, _dir)
    dirname = os.path.dirname(directory)
    file_check = Path(directory)

    # already exists?
    if file_check.is_file():
        print(f"{Log.WARNING}File already exists: {_dir}{Log.ENDC}")
        return directory

    # print(f"{Log.OKGREEN}Downloading file: {directory}{Log.ENDC}")
    # Create if not exist dir
    Path(dirname).mkdir(parents=True, exist_ok=True)
    response = session.get(uri, verify=True, timeout=60, headers={
        'User-Agent': _agents[random.randint(0, 3)]
    })

    # Check status for response
    if response.status_code == requests.codes.ok:
        # Avoid to re-download
        out = open(directory, "wb")
        for block in response.iter_content(1024):
            if not block: break
            out.write(block)
        out.close()

    print(f"{Log.OKGREEN}File stored in: {directory}{Log.ENDC}")
    return directory


def ingest_dir(_dir):
    """
    Go and conquer the world little child!!:
    :param _dir:
    :return:
    """
    directory = "%s/torrents/%s" % (root_path, _dir)
    print(f"Ingesting directory: {Log.BOLD}{_dir}{Log.ENDC}")
    _hash = ipfs.add(directory, pin=True, recursive=True)
    _hash = next(item for item in _hash if item['Name'] == _dir)['Hash']
    print(f"IPFS hash: {Log.BOLD}{_hash}{Log.ENDC}")
    return _hash


def ingest_file(uri, _dir):
    """
    Go and conquer the world little child!!
    :param uri:
    :param _dir:
    :return:
    """
    directory = download_file(uri, _dir)
    print(f"Ingesting file: {Log.BOLD}{_dir}{Log.ENDC}")
    _hash = ipfs.add(directory, pin=True)['Hash']
    print(f"IPFS hash: {Log.BOLD}{_hash}{Log.ENDC}")
    return _hash


def ingest_media(mv):
    print(f"\n{Log.OKBLUE}Ingesting {mv['imdb_code']}{Log.ENDC}")
    # Downloading files
    current_imdb_code = mv['imdb_code']
    image_index = [  # Index image movie lists
        "background_image", "background_image_original",
        "small_cover_image", "medium_cover_image",
        "large_cover_image"
    ]

    for x in image_index:  # Download all image assets
        download_file(mv[x], "%s/%s.jpg" % (current_imdb_code, x))
        del mv[x]

    for torrent in mv['torrents']:
        torrent_dir = '%s/%s/%s' % (current_imdb_code, torrent['quality'], torrent['hash'])
        download_file(torrent['url'], torrent_dir)

    # Key - Source
    for key, sub_collection in mv['subtitles'].items():
        for lang, sub_lang in sub_collection.items():  # Key - Lang
            lang_cleaned = re.sub('[^a-zA-Z0-9 \n\.]', '', lang).replace(' ', '_')
            langs_dir = f"{current_imdb_code}/subs/{lang_cleaned}"
            for sub in sub_lang:  # Iterate over links
                url_link = sub['link']
                file_name = f"{url_link.rsplit('/', 1)[-1]}.zip"
                file_dir = "%s/%s" % (langs_dir, file_name)
                download_file(url_link, file_dir)
                sub['link'] = f"{lang_cleaned}/{file_name}"

    del mv['torrents']
    del mv['_id']
    hash_directory = ingest_dir(current_imdb_code)
    mv['hash'] = hash_directory

    # Logs on ready ingested
    print(f"Hash ready for {current_imdb_code}: {hash_directory}")
    print(f"{Log.OKGREEN}Done {mv['imdb_code']}{Log.ENDC}\n")
    return mv


def process_ingestion(movies_indexed):
    with Pool(processes=10) as pool:
        p_async = pool.apply_async
        # Pool process ingest
        results = {x['imdb_code']: p_async(
            ingest_media, args=(x,)
        ) for x in movies_indexed}

        pool.close()
        pool.join()

        return {  # Generate ingestion dict
            x: y.get() for x, y in results.items()
        }


def write_subs(mongo, result, save_subs=None, index='default'):
    save_subs = save_subs or {}
    for v in result:
        # Init subs
        new_subs = {}
        x = v['imdb_code']
        old_subs = 'subtitles' in v and v['subtitles'] or {}

        # Check if subs in collection and merge it
        if x in save_subs and save_subs[x]:
            new_subs = {**old_subs, **{index: dict(save_subs[x])}}

        # Update subs
        mongo.movies.update_one(
            {'_id': v['_id']},
            {'$set': {'subtitles': new_subs}}
        )
