import os
from datetime import date
from src.core import logger, Log
from src.core import mongo
from src.core import helper
import src.core.scheme as scheme
import resolvers, asyncio

__author__ = 'gmena'
if __name__ == '__main__':

    DB_DATE_VERSION = date.today().strftime('%Y%m%d')
    ROOT_PROJECT = os.environ.get('PROJECT_ROOT', '/data/watchit')

    REFRESH_MOVIES = os.environ.get('REFRESH_MOVIES', 'False') == 'True'
    REFRESH_IPFS = os.environ.get('REFRESH_IPFS', 'False') == 'True'
    REGEN_MOVIES = os.environ.get('REGEN_MOVIES', 'False') == 'True'
    REGEN_ORBITDB = os.environ.get('REGEN_ORBITDB', 'False') == 'True'
    MIXED_RESOURCES = os.environ.get('MIXED_RESOURCES', 'False') == 'True'
    FLUSH_CACHE_IPFS = os.environ.get('FLUSH_CACHE_IPFS', 'False') == 'True'

    logger.info('Setting mongodb')
    logger.info("Running %s version in %s directory" % (DB_DATE_VERSION, ROOT_PROJECT))
    logger.info('\n')

    # Initialize db list from name
    tmp_db_name = 'witth%s' % DB_DATE_VERSION if REGEN_MOVIES else 'witth'
    temp_db, cache_db = mongo.get_dbs(tmp_db_name, 'ipfs')

    # Check for empty db
    empty_tmp = temp_db.movies.count() == 0
    empty_cache = cache_db.movies.count() == 0

    if REFRESH_MOVIES or empty_tmp:
        logger.info('Rewriting...')
        resolvers_list = resolvers.load()
        # Process each resolver and merge it
        logger.warning(f"{Log.WARNING}Running resolvers{Log.ENDC}")
        migration_result = map(helper.runtime.results_generator, resolvers_list)

        # Merge results from migrations
        logger.warning(f"{Log.WARNING}Starting merge{Log.ENDC}")
        merged_data = scheme.merge.acc_gens(migration_result)
        logger.info(f"{Log.OKGREEN}Data merge complete{Log.ENDC}")

        scheme.validator.check(merged_data, many=True)
        logger.info(f"{Log.OKGREEN}Valid scheme{Log.ENDC}")
        # Start to write obtained entries from src
        logger.info(f"{Log.OKGREEN}Inserting entries in mongo{Log.ENDC}")
        helper.rewrite_entries(temp_db, merged_data)  # Add data to helper db
        logger.info(f"{Log.UNDERLINE}Entries indexed: {len(merged_data)}{Log.ENDC}")

    empty_ = empty_cache or empty_tmp
    if REFRESH_IPFS or empty_:
        logger.info('\n')
        logger.info(f"{Log.WARNING}Starting ingestion to IPFS{Log.ENDC}")
        if FLUSH_CACHE_IPFS or empty_:
            helper.runtime.flush_ipfs(cache_db, temp_db)

        # Get stored movies data and process it
        migration_result = temp_db.movies.find({
            "updated": {'$exists': False}
        }, no_cursor_timeout=True).batch_size(1000)

        # Start IPFS ingestion
        helper.init_ingestion(
            cache_db, temp_db,
            migration_result
        )

    # Add resolvers if not mixed allowed
    resolvers_names = not MIXED_RESOURCES and list(map(
        helper.runtime.resolvers_to_str, resolvers.load()
    )) or None

    # Start node subprocess migration
    asyncio.run(helper.call_orbit_subprocess(
        resolvers=resolvers_names,  # Add resolvers if not mixed allowed
        regen=REGEN_ORBITDB,  # Regen orbit directory
    ))
    exit(0)
