import click
from src.sdk.scheme.validator import check
from src.sdk import cache, exception, logger, web3
from src.sdk.exec import w3 as w3_exec
from src.sdk.exception import InvalidCID


@click.group("w3")
@click.option("--network", default=4)
@click.pass_context
def w3(ctx, network):
    """Web3 toolkit"""
    ctx.ensure_object(dict)
    # TODO if network is string convert to chain id
    ctx.obj["network"] = network


@w3.command()
@click.pass_context
def status(ctx):
    """Check for network status"""
    context_network = ctx.obj["network"]
    w3 = web3.factory.w3(context_network)
    logger.log.success(
        f"{context_network} connected"
    ) if w3.isConnected() else logger.log.error(f"{context_network} offline")


@w3.command()
@click.pass_context
@click.option("--address")
def tx(ctx, address):
    """Tx status"""
    context_network = ctx.obj["network"]
    w3 = web3.factory.w3(context_network)
    web3.tx.status(w3, address)


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
def cached(ctx, skip, limit):
    """Batch mint from ingested cache cid list \n
    Note: Please ensure that binaries are already ingested before run this command.
    eg. Resolve meta -> Transcode media -> Generate NFT metadata -> ingest -> mint batch
    """
    result, result_count = cache.ingest.frozen()
    result = result.skip(skip).limit(limit)
    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    context_network = ctx.obj["network"]
    # Get hash list from ingested cursor db
    cid_list = list(map(lambda x: x["hash"], result))

    # Wrap w3 and get account from private key
    w3 = web3.factory.w3(context_network)
    to = web3.factory.account(w3).address
    tx, to, cid_list = web3.nft.mint_batch(to, cid_list, context_network)
    cache.mint.freeze(tx, to, cid_list)


@mint.command()
@click.option("--cid", default=None)
@click.pass_context
def single(ctx, cid):
    """Mint arbitrary cid"""
    if not cid:
        raise InvalidCID()

    context_network = ctx.obj["network"]
    # Wrap w3 and get account from private key
    w3 = web3.factory.w3(context_network)
    to = web3.factory.account(w3).address
    tx, to, cid = web3.nft.mint(to, cid, context_network)
    cache.mint.freeze(tx, to, [cid])


@nft.group("generate")
def generate():
    pass


@generate.command()
def erc1155():
    """Generate metadata json file for ERC1155 NFT \n
    Note: Please ensure that media is already transcode before run this command.
    eg. Resolve meta -> Transcode/Static -> generate
    """
    # Return available and not processed entries
    # Total size of entries to fetch
    result, _ = cache.manager.safe_retrieve()
    # Generate metadata file from each row in tmp db the resources
    for current_movie in check(result):
        w3_exec.boot(current_movie)
