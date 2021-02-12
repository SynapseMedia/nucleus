import os
from datetime import date
from src.core import logger, Log
from src.core import mongo
from src.core import helper
import src.core.scheme as scheme
import resolvers

__author__ = 'gmena'
if __name__ == '__main__':

    DB_DATE_VERSION = date.today().strftime('%Y%m%d')
    ROOT_PROJECT = os.environ.get('PROJECT_ROOT', '/data/watchit')

    REFRESH_MOVIES = os.environ.get('REFRESH_MOVIES', 'False') == 'True'
    REFRESH_IPFS = os.environ.get('REFRESH_IPFS', 'False') == 'True'
    REGEN_MOVIES = os.environ.get('REGEN_MOVIES', 'False') == 'True'
    REGEN_ORBITDB = os.environ.get('REGEN_ORBITDB', 'False') == 'True'
    FLUSH_CACHE_IPFS = os.environ.get('FLUSH_CACHE_IPFS', 'False') == 'True'

    logger.info('Setting mongodb')
    logger.info("Running %s version in %s directory" % (DB_DATE_VERSION, ROOT_PROJECT))
    logger.info('\n')

    # Process each resolver and merge it
    for resolver in resolvers.load():
        _resolver = resolver(scheme)  # Init class with scheme
        logger.info(f"{Log.BOLD}Starting migrations from {_resolver} {DB_DATE_VERSION}{Log.ENDC}")
        migration_result = _resolver()  # Call class and start migration
        logger.info(migration_result)
        # scheme.validator.check(migration_result)

        logger.info(f"{Log.OKGREEN}Migration Complete for {_resolver}{Log.ENDC}")
        # logger.info(f"{Log.OKGREEN}Inserting entries in mongo{Log.ENDC}")

    exit(0)
    # Initialize db list from name
    tmp_db_name = 'witth%s' % DB_DATE_VERSION if REGEN_MOVIES else 'witth'
    temp_db, cache_db = mongo.get_dbs(tmp_db_name, 'ipfs')

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
        helper.rewrite_entries(temp_db, migration_result)
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
        helper.init_ingestion(cache_db, temp_db, migration_result)

    # Start node subprocess migration
    helper.call_orbit_subprocess(REGEN_ORBITDB)
    exit(0)
