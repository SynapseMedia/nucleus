import os
from datetime import date
from pymongo import MongoClient, InsertOne
from subprocess import call

from resource.py import Log
from resource.py.subs.opensubs import migrate as OSubs
from resource.py.subs.yifisubs import YSubs
from resource.py.torrents.yts import YTS
from resource.py.media.ingest import write_subs

__author__ = 'gmena'
if __name__ == '__main__':

    DB_DATE_VERSION = date.today().strftime('%Y%m%d')
    MONGO_HOST, MONGO_PORT = ('mongodb', '27017')
    ROOT_PROJECT = os.environ.get('PROJECT_ROOT', '/data/watchit')
    START_PAGE = int(os.environ.get('START_PAGE', 0))
    STEP_PAGE = int(os.environ.get('STEP_PAGE', 50))
    REFRESH_MOVIES = os.environ.get('REFRESH_MOVIES', 'False') == 'True'
    REFRESH_SUBS = os.environ.get('REFRESH_SUBS', 'False') == 'True'

    # CLI
    _root_api = 'https://yts.mx'
    # Initialize yts.ag
    yts = YTS(
        host='%s/api/v2/list_movies.json' % _root_api,
        page=START_PAGE, limit=STEP_PAGE
    )

    # Setting mongo
    print('\nSetting mongodb')
    print("Running %s version in %s directory" % (DB_DATE_VERSION, ROOT_PROJECT))
    _mongo_db = MongoClient('mongodb://' + MONGO_HOST + ':' + str(MONGO_PORT) + '/witth')
    _mongo_db = _mongo_db['witth']
    _migration_result = []

    # If clean
    empty_mongo = _mongo_db.movies.find({}).count() == 0
    if REFRESH_MOVIES or empty_mongo:
        print('Rewriting...')
        print(f"\n{Log.BOLD}Starting migrations from yts.mx {DB_DATE_VERSION}{Log.ENDC}")
        # The result of migration
        _migration_result = yts.migrate(resource_name='yts')
        print(f"{Log.OKGREEN}Migration Complete for yts.ag{Log.ENDC}")
        print(f"{Log.OKGREEN}Inserting entries in mongo{Log.ENDC}")
        _mongo_db.movies.delete_many({})  # Clean all
        _mongo_bulk = [InsertOne(i) for k, i in _migration_result.items()]
        _mongo_db.movies.bulk_write(_mongo_bulk)

    if REFRESH_SUBS or empty_mongo:
        # Process subs for each movie
        print(f"\n{Log.WARNING}Starting migration from yify subtitles{Log.ENDC}")
        migration_result = list(_mongo_db.movies.find({}))
        ysubs = YSubs(host='http://www.yifysubtitles.com')
        subs_lists_yifi = ysubs.migrate(migration_result)
        print(f"{Log.OKGREEN}Migration Complete for yifi subtitles{Log.ENDC}")
        print(f"{Log.OKGREEN}Merging YTS subs{Log.ENDC}")
        write_subs(_mongo_db, migration_result, subs_lists_yifi, 'yifi')

    if REFRESH_SUBS or empty_mongo:
        print(f"\n{Log.WARNING}Starting migration from open subtitles{Log.ENDC}")
        migration_result = list(_mongo_db.movies.find({}))
        subs_lists_open = OSubs(migration_result)
        print(f"{Log.OKGREEN}Migration Complete for open subtitles{Log.ENDC}")
        print(f"{Log.OKGREEN}Save in Mongo OpenSub subs{Log.ENDC}")
        _migration_result = list(_mongo_db.movies.find({}))
        write_subs(_mongo_db, migration_result, subs_lists_open, 'opensubs')

    print(f"\n{Log.BOLD}Migration Complete:{Log.ENDC}")
    print(f"{Log.UNDERLINE}Entries yts indexed: {len(_migration_result)}{Log.ENDC}")

    # Spawn node subprocess
    call(["node", "%s/resource/orbit/migrate.js" % ROOT_PROJECT, MONGO_HOST], shell=False)
