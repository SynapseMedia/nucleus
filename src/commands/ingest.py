import click
from src.sdk.scheme.validator import check
from src.sdk import cache, mongo, logger, exception, media
from src.sdk.constants import FLUSH_CACHE_IPFS, AUTO_PIN_FILES


def _pin_files():
    """
    Pin ingested file from cursor cache db
    :return:
    """
    logger.log.warning("Starting pinning to IPFS")
    entries, _ = cache.retrieve()
    files_cid = map(lambda x: x["hash"], entries)
    media.ingest.pin_cid_list(files_cid)
    entries.close()


@click.command()
@click.option("--no-cache", default=FLUSH_CACHE_IPFS)
@click.option("--pin", default=AUTO_PIN_FILES)
def ingest(no_cache, pin):
    """
    Ingest media ready for production into IPFS
    """
    media.ingest.ipfs = media.ingest.start_node()  # Init ipfs node
    logger.log.warning("Starting ingestion to IPFS")
    if no_cache or mongo.empty_tmp:  # Clean already ingested cursor
        cache.flush()

    # Total size of entries to fetch
    # Return available and not processed entries
    result, result_count = cache.pending()

    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    logger.log.notice(f"Ingesting {result_count} results")
    logger.log.info("\n")

    # Ingest from each row in tmp db the resources
    for current_movie in check(result):
        _id = current_movie.imdb_code  # Current id
        ingested_data = media.ingest.to_ipfs_from(current_movie)
        cache.set_ingested_with(_id, ingested_data)

    if pin:  # If allowed pin files
        _pin_files()

    result.close()
