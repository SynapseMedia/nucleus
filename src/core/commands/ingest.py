import click, os
from src.core import logger, Log
import src.core.mongo as mongo
import src.core.helper as helper

REFRESH_IPFS = os.getenv('REFRESH_IPFS', 'False') == 'True'
FLUSH_CACHE_IPFS = os.getenv('FLUSH_CACHE_IPFS', 'False') == 'True'


@click.command()
@click.option('--refresh', default=REFRESH_IPFS)
@click.option('--flush-ipfs', default=REFRESH_IPFS)
def ingest(refresh, clean_ipfs):
    """
    Add media ready for prod into IPFS
    :return:
    """
    all_empty_cache = mongo.empty_tmp or mongo.empty_cursor
    if refresh or all_empty_cache:
        logger.info('\n')
        logger.info(f"{Log.WARNING}Starting ingestion to IPFS{Log.ENDC}")
        if clean_ipfs or all_empty_cache:
            helper.runtime.flush_ipfs(cache_db, temp_db)
