import click
import os
from src.core import logger
import src.core.mongo as mongo
import src.core.helper as helper
import src.core.media as media
import src.core.exception as exceptions

FLUSH_CACHE_IPFS = os.getenv("FLUSH_CACHE_IPFS", "False") == "True"
AUTO_PIN_FILES = os.getenv("AUTO_PIN_FILES", "False") == "True"


def _pin_files(cursor_db):
    """
    Pin ingested file from cursor cache db
    :param cursor_db:
    :return:
    """
    logger.warning(f"Starting pinning to IPFS")
    entries = helper.cache.retrieve(cursor_db)
    files_cid = map(lambda x: x["hash"], entries)
    media.ingest.ipfs_pin_cid(files_cid)
    entries.close()


@click.command()
@click.option("--no-cache", default=FLUSH_CACHE_IPFS)
@click.option("--pin", default=AUTO_PIN_FILES)
def ingest(no_cache, pin):
    """
    Ingest media ready for production into IPFS
    """
    media.ingest.start_node()  # Init ipfs node
    logger.warning(f"Starting ingestion to IPFS")
    if no_cache or mongo.empty_tmp:  # Clean already ingested cursor
        helper.cache.flush_ipfs(mongo.cursor_db, mongo.temp_db)

    # Return available and not processed entries
    result = helper.cache.retrieve(mongo.temp_db, {"updated": {"$exists": False}})
    result_count = result.count()  # Total size of entries to fetch

    if result_count == 0:  # If not data to fetch
        raise exceptions.EmptyCache()

    logger.notice(f"Ingesting {result_count} results")
    logger.info(f"\n")

    # Ingest from each row in tmp db the resources
    for current_movie in result:
        _id = current_movie["_id"]  # Current id
        ingested_data = media.ingest.ipfs_metadata(current_movie)
        mongo.cursor_db.movies.insert_one(ingested_data)
        mongo.temp_db.movies.update_one({"_id": _id}, {"$set": {"updated": True}})

    if pin:  # If allowed pin files
        _pin_files(mongo.cursor_db)

    result.close()
