import os
from datetime import date

from src.core import logger, Log
from src.core import media
from src.core import mongo
import resolvers

__author__ = 'gmena'
if __name__ == '__main__':

    DB_DATE_VERSION = date.today().strftime('%Y%m%d')
    ROOT_PROJECT = os.environ.get('PROJECT_ROOT', '/data/watchit')

    REFRESH_MOVIES = os.environ.get('REFRESH_MOVIES', 'False') == 'True'
    REFRESH_IPFS = os.environ.get('REFRESH_IPFS', 'False') == 'True'
    FLUSH_CACHE_IPFS = os.environ.get('FLUSH_CACHE_IPFS', 'False') == 'True'


    def init_ingestion(idb, wdb, movies_indexed):
        """
        Start ingestion for each movie
        Request, download and add files to ipfs then save as cache in mongo
        :param idb: Cache ipfs db to hold cursor
        :param wdb: Temp movies db with all movies stored from resources
        :param movies_indexed:
        :return:
        """
        for x in movies_indexed:
            _id = x['_id']  # Current id
            ingested_data = media.ingest_ipfs_metadata(x)
            if 'torrents' not in x:
                continue
            idb.movies.insert_one(ingested_data)
            wdb.movies.update_one({'_id': _id}, {'$set': {'updated': True}})
        movies_indexed.close()


    def rewrite_entries(db, data):
        """
        Just remove old data and replace it with new data
        :param db:
        :param data:
        :return:
        """
        db.movies.delete_many({})  # Clean all
        bulk = [mongo.InsertOne(i) for k, i in data.items()]
        db.movies.bulk_write(bulk)


    logger.info('Setting mongodb')
    logger.info("Running %s version in %s directory" % (DB_DATE_VERSION, ROOT_PROJECT))
    logger.info('\n')
    # Initialize db list from name
    temp_db, cache_db = mongo.get_dbs('witth', 'ipfs')

    # Check for empty db
    empty_tmp = temp_db.movies.count() == 0
    empty_cache = cache_db.movies.count() == 0

    if REFRESH_MOVIES or empty_tmp:
        logger.info('Rewriting...')
        logger.info(f"{Log.BOLD}Starting migrations from yts.mx {DB_DATE_VERSION}{Log.ENDC}")

        # Process each resolver and merge it
        # for resolver in resolvers.RESOLVERS_LIST:
        migration_result = resolvers.yts.YTS()()
        logger.info(f"{Log.OKGREEN}Migration Complete for yts.ag{Log.ENDC}")
        logger.info(f"{Log.OKGREEN}Inserting entries in mongo{Log.ENDC}")

        # Start to write obtained entries from src
        rewrite_entries(temp_db, migration_result)
        logger.info(f"{Log.UNDERLINE}Entries yts indexed: {len(migration_result)}{Log.ENDC}")

    if REFRESH_IPFS or empty_cache:
        logger.info('\n')
        logger.info(f"{Log.WARNING}Starting ingestion to IPFS{Log.ENDC}")
        if FLUSH_CACHE_IPFS or empty_cache:
            # Reset old entries and restore it
            cache_db.movies.delete_many({})
            temp_db.movies.update_many(
                {"updated": True},
                {'$unset': {"updated": None}}
            )

        # Start IPFS ingestion
        # Get stored movies data and process it
        migration_result = temp_db.movies.find({
            "updated": {'$exists': False}
        }, no_cursor_timeout=True).batch_size(1000)
        init_ingestion(cache_db, temp_db, migration_result)

        # Spawn node subprocess
        # call(["node", "%s/src/orbit/migrate.js" % ROOT_PROJECT, MONGO_HOST], shell=False)
