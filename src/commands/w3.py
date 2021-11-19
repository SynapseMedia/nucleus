import click
from src.sdk.scheme.validator import check
from src.sdk import cache, media, exception, logger, util, web3
from src.sdk.exception import InvalidCID


@click.group("w3")
@click.option("--network", default="rinkeby")
@click.pass_context
def w3(ctx, network):
    """Web3 toolkit"""
    ctx.ensure_object(dict)
    ctx.obj["network"] = network


@w3.command()
@click.pass_context
def status(ctx):
    """Check for network status"""
    context_network = ctx.obj["network"]
    _w3 = web3.factory.w3(context_network)
    logger.log.success(
        f"{context_network} connected"
    ) if _w3.isConnected() else logger.log.error(f"{context_network} offline")


@w3.group("nft")
@click.pass_context
def nft(_):
    """NFT toolkit"""
    pass


@nft.group("mint")
@click.pass_context
def mint(ctx):
    pass


@mint.command()
@click.option("--skip", default=0)
@click.option("--limit", default=0)
@click.pass_context
def batch(ctx, skip, limit):
    """Batch mint from ingested cache cid list \n
    Note: Please ensure that binaries are already ingested before run this command.
    eg. Resolve meta -> Transcode media -> Generate NFT metadata -> ingest -> mint batch
    """
    result, result_count = cache.ingested()
    result = result.skip(skip).limit(limit)
    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    context_network = ctx.obj["network"]
    # Get hash list from ingested cursor db
    cid_list = list(map(lambda x: x["hash"], result))

    _w3 = web3.factory.w3(context_network)
    _to = _w3.eth.account.privateKeyToAccount(web3.factory.WALLET_KEY).address
    tx, to, cid_list = web3.nft.mint_batch(_to, cid_list, context_network)
    cache.freeze(tx, to, cid_list)


@mint.command()
@click.option("--cid", default=None)
@click.pass_context
def single(ctx, cid):
    """Mint arbitrary cid"""
    if not cid:
        raise InvalidCID()

    context_network = ctx.obj["network"]
    _w3 = web3.factory.w3(context_network)
    _to = _w3.eth.account.privateKeyToAccount(web3.factory.WALLET_KEY).address
    tx, to, cid = web3.nft.mint(_to, cid, context_network)
    cache.freeze(tx, to, [cid])


@nft.command()
def generate():
    """Generate metadata json file for ERC1155 NFT \n
    Note: Please ensure that media is already transcode before run this command.
    eg. Resolve meta -> Transcode media -> generate
    """
    # Return available and not processed entries
    # Total size of entries to fetch
    metadata_list = []
    metadata_list_append = metadata_list.append
    result, _ = cache.safe_retrieve()
    # Generate metadata file from each row in tmp db the resources
    for current_movie in check(result):
        logger.log.warning(f"Processing NFT meta for {current_movie.imdb_code}")
        # Build metadata for current movie
        nft_movie_meta = media.nft.erc1155_metadata(current_movie)
        metadata_list_append(nft_movie_meta)
        # Get directory output for current movie meta json
        current_dir = util.build_dir(current_movie)
        directory, _ = util.resolve_root_for(current_dir)
        util.write_json(f"{directory}/index.json", nft_movie_meta)
        logger.log.success(f"Written metadata for {current_movie.imdb_code}\n")
