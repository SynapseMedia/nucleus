import ipfshttpclient, csv, time
from resource.py import Log
from resource.py.media.download import root_path, download_file, download_scrap_subs, API_NEEDED
from resource.py.subs.opensubs import OPEN_SUBS_RECURSIVE_SLEEP_REQUEST

__author__ = 'gmena'

try:
    ipfs = ipfshttpclient.connect('/dns/ipfs/tcp/5001/http', session=True)
    print(ipfs.id())
except ipfshttpclient.exceptions.ConnectionError:
    pass


def get_pb_domain_set(csv_file='pdm.csv'):
    with open(f"{root_path}/{csv_file}", 'r') as f:
        reader = csv.reader(f)
        return set([row[1] for row in reader])


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
    """
    Loop over assets, download it and add it to IPFS
    :param mv:
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

        # Key - Source
        for key, sub_collection in mv['subtitles'].items():
            if key in API_NEEDED:
                # API_NEEDED[key](  # Switch to API handler
                #     current_imdb_code,
                #     sub_collection
                # )
                continue

            # Otherwise process all scrapped links
            download_scrap_subs(
                current_imdb_code,
                sub_collection
            )

        hash_directory = ingest_dir(current_imdb_code)
        mv['hash'] = hash_directory
        # Logs on ready ingested
        print(f"{Log.OKGREEN}Done {mv['imdb_code']}{Log.ENDC}\n")
        return mv
    except Exception as e:
        print('Retry download assets error:', e)
        print("\n\033[93mWait", str(OPEN_SUBS_RECURSIVE_SLEEP_REQUEST), 'seconds\033[0m\n')
        time.sleep(OPEN_SUBS_RECURSIVE_SLEEP_REQUEST)
        return ingest_media(mv)


def process_ingestion(ipfs_db, mongo, movies_indexed):
    for x in movies_indexed:
        _id = x['_id']  # Current id
        ingested_data = ingest_media(x)
        ipfs_db.movies.insert_one(ingested_data)
        mongo.movies.update({'_id': _id}, {'$set': {'updated': True}})
    movies_indexed.close()


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
