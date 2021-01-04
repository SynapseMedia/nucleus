import os
from datetime import date
from pymongo import MongoClient, InsertOne
# from subprocess import call

from resource.py import Log
from resource.py.media.ingest import write_subs, process_ingestion
from resource.py.subs.opensubs import migrate as OSubs
from resource.py.subs.yifisubs import YSubs
from resource.py.torrents.yts import YTS

__author__ = 'gmena'
if __name__ == '__main__':

    DB_DATE_VERSION = date.today().strftime('%Y%m%d')
    MONGO_HOST, MONGO_PORT = ('mongodb', '27017')
    ROOT_PROJECT = os.environ.get('PROJECT_ROOT', '/data/watchit')
    START_PAGE = int(os.environ.get('START_PAGE', 0))
    STEP_PAGE = int(os.environ.get('STEP_PAGE', 50))
    REFRESH_MOVIES = os.environ.get('REFRESH_MOVIES', 'False') == 'True'
    REFRESH_IPFS = os.environ.get('REFRESH_IPFS', 'False') == 'True'
    REFRESH_SUBS = os.environ.get('REFRESH_SUBS', 'False') == 'True'
    FLUSH_CACHE_IPFS = os.environ.get('FLUSH_CACHE_IPFS', 'False') == 'True'

    # CLI
    _root_api = 'https://yts.mx'
    _client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
    # Initialize yts.ag
    yts = YTS(
        host='%s/api/v2/list_movies.json' % _root_api,
        page=START_PAGE, limit=STEP_PAGE
    )


    def rewrite_entries(r_db, data):
        r_db.movies.delete_many({})  # Clean all
        bulk = [InsertOne(i) for k, i in data.items()]
        r_db.movies.bulk_write(bulk)


    # Setting mongo
    print('\nSetting mongodb')
    print("Running %s version in %s directory" % (DB_DATE_VERSION, ROOT_PROJECT))
    _mongo_db = _client['witth']
    _ipfs_db = _client['ipfs']
    _migration_result = []

    # If empty db
    empty_mongo = _mongo_db.movies.find({}).count() == 0
    empty_ipfs = _ipfs_db.movies.find({}).count() == 0

    if REFRESH_MOVIES or empty_mongo:
        print('Rewriting...')
        print(f"\n{Log.BOLD}Starting migrations from yts.mx {DB_DATE_VERSION}{Log.ENDC}")
        # The result of migration
        migration_result = yts.migrate(resource_name='yts')
        print(f"{Log.OKGREEN}Migration Complete for yts.ag{Log.ENDC}")
        print(f"{Log.OKGREEN}Inserting entries in mongo{Log.ENDC}")
        rewrite_entries(_mongo_db, migration_result)
        print(f"{Log.UNDERLINE}Entries yts indexed: {len(migration_result)}{Log.ENDC}")

    if REFRESH_SUBS or empty_mongo:
        # Process subs for each movie
        print(f"\n{Log.WARNING}Starting migration from yify subtitles{Log.ENDC}")
        migration_result = _mongo_db.movies.find({})
        ysubs = YSubs(host='http://www.yifysubtitles.com')
        subs_lists_yifi = ysubs.migrate(migration_result)
        print(f"{Log.OKGREEN}Migration Complete for yifi subtitles{Log.ENDC}")
        print(f"{Log.OKGREEN}Merging YTS subs{Log.ENDC}")
        write_subs(_mongo_db, migration_result, subs_lists_yifi, 'yifi')

    if REFRESH_SUBS or empty_mongo:
        print(f"\n{Log.WARNING}Starting migration from open subtitles{Log.ENDC}")
        migration_result = _mongo_db.movies.find({})
        subs_lists_open = OSubs(migration_result)
        print(f"{Log.OKGREEN}Migration Complete for open subtitles{Log.ENDC}")
        print(f"{Log.OKGREEN}Save in Mongo OpenSub subs{Log.ENDC}")
        write_subs(_mongo_db, migration_result, subs_lists_open, 'opensubs')

    if REFRESH_IPFS or empty_ipfs:
        print(f"\n{Log.WARNING}Starting ingestion to IPFS{Log.ENDC}")
        if FLUSH_CACHE_IPFS or empty_ipfs:
            # Reset old entries and restore it
            _ipfs_db.movies.delete_many({})
            _mongo_db.movies.update_many({"updated": True}, {'$unset': {"updated": None}})
        # Start IPFS ingestion
        # Get stored movies data and process it
        migration_result = _mongo_db.movies.find({
            "updated": {'$exists': False}
        }, no_cursor_timeout=True).batch_size(1000)
        process_ingestion(_ipfs_db, _mongo_db, migration_result)

    # Spawn node subprocess
    # call(["node", "%s/resource/orbit/migrate.js" % ROOT_PROJECT, MONGO_HOST], shell=False)
