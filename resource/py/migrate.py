import os
from datetime import date
from pymongo import MongoClient, InsertOne
from subprocess import call

from resource.py import Log
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
    REFRESH_SUBS = os.environ.get('REFRESH_SUBS', 'False') == 'True'
    print("\nRunning %s version in %s directory" % (DB_DATE_VERSION, ROOT_PROJECT))

    # CLI
    _root_api = 'https://yts.mx'
    # Initialize yts.ag
    yts = YTS(
        host='%s/api/v2/list_movies.json' % _root_api,
        page=START_PAGE, limit=STEP_PAGE
    )

    # Setting mongo
    print('\nSetting mongodb')
    _mongo = MongoClient('mongodb://' + MONGO_HOST + ':' + str(MONGO_PORT) + '/witth' + DB_DATE_VERSION)
    _mongo_db = _mongo['witth' + DB_DATE_VERSION]
    _migration_result = []


    def write_subs(result, save_subs=None, index='default'):
        save_subs = save_subs or {}
        for v in result:
            # Init subs
            new_subs = {}
            x = v['imdb_code']
            old_subs = 'subtitles' in v and v['subtitles'] or {}

            if x in save_subs and save_subs[x]:
                new_subs = {**old_subs, **{index: dict(save_subs[x])}}

            _mongo_db.movies.update_one(
                {'_id': v['_id']},
                {'$set': {'subtitles': new_subs}}
            )


    # If clean
    empty_mongo = _mongo_db.movies.find({}).count() == 0
    if REFRESH_MOVIES or empty_mongo:
        print('Rewriting...')
        print(f"\n{Log.WARNING}Starting migrations from yts.mx {DB_DATE_VERSION}{Log.ENDC}")
        # The result of migration
        _migration_result = yts.migrate(resource_name='yts')
        print(f"\n{Log.OKGREEN}Migration Complete for yts.ag{Log.ENDC}")
        print(f"\n{Log.OKGREEN}Inserting entries in mongo{Log.ENDC}")
        _mongo_db.movies.delete_many({})  # Clean all
        _mongo_bulk = [InsertOne(i) for k, i in _migration_result.items()]
        _mongo_db.movies.bulk_write(_mongo_bulk)

    if REFRESH_SUBS or empty_mongo:
        # Process subs for each movie
        print(f"\n{Log.WARNING}Starting migration from yify subtitles{Log.ENDC}")
        migration_result = list(_mongo_db.movies.find({}))
        ysubs = YSubs(host='http://www.yifysubtitles.com')
        subs_lists_yifi = ysubs.migrate(migration_result)
        print(f"\n{Log.OKGREEN}Migration Complete for yifi subtitles{Log.ENDC}")
        print(f"\n{Log.OKGREEN}Merging YTS subs{Log.ENDC}")
        write_subs(migration_result, subs_lists_yifi, 'yifi')

    if REFRESH_SUBS or empty_mongo:
        print(f"\n{Log.WARNING}Starting migration from open subtitles{Log.ENDC}")
        migration_result = list(_mongo_db.movies.find({}))
        subs_lists_open = OSubs(migration_result)
        print(f"\n{Log.OKGREEN}Migration Complete for open subtitles{Log.ENDC}")
        print(f"\n{Log.OKGREEN}Save in Mongo OpenSub subs{Log.ENDC}")
        _migration_result = list(_mongo_db.movies.find({}))
        write_subs(migration_result, subs_lists_open, 'opensubs')

    print(f"{Log.BOLD}Migration Complete:{Log.ENDC}")
    print(f"{Log.UNDERLINE}Entries yts indexed: {len(_migration_result)}{Log.ENDC}")

    # Spawn node subprocess
    call(["node", "%s/resource/orbit/migrate.js" % ROOT_PROJECT, MONGO_HOST, DB_DATE_VERSION], shell=False)
