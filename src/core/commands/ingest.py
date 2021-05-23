import click, os
from src.core import logger, Log
import src.core.mongo as mongo
import src.core.helper as helper
import src.core.media as media

REFRESH_IPFS = os.getenv('REFRESH_IPFS', 'False') == 'True'


@click.command()
@click.option('--refresh', default=REFRESH_IPFS)
def ingest(refresh):
    """
    Add media ready for prod into IPFS
    :return:
    """
    if refresh or mongo.empty_tmp:
        logger.info(f"{Log.WARNING}Starting ingestion to IPFS{Log.ENDC}")
        helper.runtime.flush_ipfs(mongo.cursor_db, mongo.temp_db)
        result = helper.cache.retrieve_not_processed(mongo.temp_db)
        result_count = result.count()  # Total size of entries to fetch
        logger.info(f"{Log.WARNING}Ingesting {result_count} results{Log.ENDC}")

        # Ingest from each row in tmp db the resources
        for current_movie in result:
            _id = current_movie['_id']  # Current id
            ingested_data = media.ingest.ipfs_metadata(current_movie)
            mongo.cursor_db.movies.insert_one(ingested_data)
            mongo.temp_db.movies.update_one({'_id': _id}, {'$set': {'updated': True}})

        result.close()
