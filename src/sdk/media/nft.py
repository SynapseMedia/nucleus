from src.sdk import util, logger
from src.sdk.scheme.definition.nft import MovieNFTProperties, MovieNFT
from src.sdk.scheme.definition.movies import MovieScheme


def nft_erc1155_metadata(mv: MovieScheme):
    """
    Go and conquer the world little child!!:
    Add directory to ipfs
    :param mv: MovieScheme
    :return: The resulting CID
    """

    logger.log.warning(f"Processing NFT meta for {mv.get('imdb_code')}")
    # Logs on ready ingested
    current_dir = util.build_dir(mv)
    directory, path_exists = util.resolve_root_for(current_dir)
    nft_movies_properties = MovieNFTProperties(name=mv.title, description=mv.synopsis)
    nft_movie = MovieNFT(title="WNFT Metadata", type="object").build(
        nft_movies_properties
    )

    util.write_json(directory, nft_movie)
    logger.log.success(f"Written metadata for {mv.imdb_code}\n")
