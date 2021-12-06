import click
from src.sdk.scheme.validator import check
from src.sdk import cache, logger, exception, media
from src.sdk.constants import FLUSH_CACHE_IPFS
from src.sdk.exception import InvalidCID


def _pin_cid_list(cid_list, remote_strategy=True):
    """
    Pin ingested cid list
    :param cid_list: List of cid to pin
    :param remote_strategy: Pin remote or local
    :return:
    """
    logger.log.warning("Starting pinning to IPFS")
    if remote_strategy:
        media.storage.ingest.pin_cid_list_remote(cid_list)
        exit(0)  # Success termination
    media.storage.ingest.pin_cid_list(cid_list)


@click.group("storage")
@click.pass_context
def storage(ctx):
    """Storage toolkit"""
    pass


@storage.command()
@click.option("--no-cache", default=FLUSH_CACHE_IPFS, is_flag=True)
@click.pass_context
def ingest(ctx, no_cache):
    """
    Ingest media ready for production into IPFS. \n
    Note: Please ensure that binaries is pre-processed before run this command.
    eg. Resolve meta -> Transcode media -> Generate NFT metadata -> ingest
    """
    media.storage.init()  # Init ipfs node
    logger.log.warning("Starting ingestion to IPFS")
    if no_cache or cache.empty_tmp:  # Clean already ingested cursor
        cache.manager.flush()

    # Total size of entries to fetch
    # Return available and not processed entries
    result, result_count = cache.ingest.pending()
    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    logger.log.notice(f"Ingesting {result_count} results")
    logger.log.info("\n")

    # Ingest from each row in tmp db the resources
    for current_movie in check(result):
        _id = current_movie.imdb_code  # Current id
        ingested_data = media.storage.ingest.to_ipfs(current_movie)
        cache.ingest.freeze(_id, ingested_data)


@storage.group("edge")
@click.pass_context
def edge(ctx):
    """Edge cache"""
    pass


@edge.command()
@click.pass_context
def status(ctx):
    """Check for edge cache status"""
    media.storage.init()  # Init ipfs node
    is_edge_active = media.storage.remote.check_status()
    if is_edge_active:
        logger.log.success("Edge cache: Success")
        exit(0)  # Success termination
    logger.log.error("Edge cache: Offline")


@edge.group("pin")
@click.option("--remote", default=True, is_flag=True)
@click.pass_context
def pin(ctx, remote):
    """Pin cid tools"""
    ctx.ensure_object(dict)
    ctx.obj["remote"] = remote
    pass


@pin.command()
@click.option("--cid", default=None)
@click.pass_context
def single(ctx, cid):
    """Pin arbitrary cid"""
    if not cid:
        raise InvalidCID()

    media.storage.init()  # Init ipfs node
    logger.log.warning(f"Start pinning for cid: {cid}")
    _pin_cid_list([cid], ctx.obj["remote"])


@pin.command()
@click.option("--skip", default=0)
@click.option("--limit", default=0)
@click.pass_context
def batch(ctx, skip, limit):
    """Pin batch cid from ingested cache cid list \n
    Note: Please ensure that binaries are already ingested before run this command.
    eg. Resolve meta -> Transcode media -> Generate NFT metadata -> ingest -> pin batch
    """
    media.storage.init()  # Init ipfs node
    entries, _ = cache.ingest.frozen()  # Retrieve already ingested cid list
    entries = entries.skip(skip).limit(limit)
    cid_list = map(lambda x: x["hash"], entries)
    _pin_cid_list(cid_list, ctx.obj["remote"])
