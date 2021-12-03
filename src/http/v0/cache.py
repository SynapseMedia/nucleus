from flask import jsonify, request, Blueprint
from src.sdk.cache import ingest, mint, manager, DESCENDING
from src.sdk.media.metadata import generate_erc1155
from src.sdk.scheme.validator import check
from src.sdk.constants import NODE_URI, API_VERSION
from itertools import zip_longest

cache_ = Blueprint("cache", __name__)


def _sanitize_internals(entry):
    """
    Re-struct response cleaning internal data
    :param entry: MovieScheme dict
    :return MovieScheme dict with cleaned and sanitized fields
    """

    # Clean not public data
    del entry['hash']  # remove needed pre processing field
    del entry['cid']  # remove needed association field
    del entry["properties"]["properties"]["hash"]
    del entry["properties"]["properties"]["resource"]
    # Movie imdb_code to get sanitize URI
    image = entry['properties']['image']
    # Sanitize uri to get handled by proxy
    movie_path = f"/{entry['tx']}/{entry['id']}"
    new_image_path = f"{NODE_URI}/{API_VERSION}/proxy{movie_path}{image}"

    # Set paths for assets and nav
    entry['properties']['path'] = movie_path
    entry["properties"]["image"] = new_image_path
    return entry


@cache_.route("/recent", methods=["GET"])
def recent():
    order_by = request.args.get("order", DESCENDING)
    limit = request.args.get("limit", 10)

    # Get current latest minted movies
    minted_nft, _ = mint.frozen({}, {"cid": 1, "tx": 1, "id": 1, "_id": False})
    minted_nft_limited = list(minted_nft.limit(limit))  # slice response
    mapped_cid = map(lambda x: x.get("cid"), minted_nft_limited)

    # Parse erc1155 metadata
    # Get "in-relation" hash from ingested metadata
    metadata_for_cid, _ = ingest.frozen({"hash": {"$in": tuple(mapped_cid)}})
    metadata_for_cid.sort([("_id", order_by)])  # sort descending by date

    # Generate metadata ERC1155 for response
    movies_meta = list(map(generate_erc1155, check(metadata_for_cid)))
    # Sort to zip entries with correspondence
    movies_meta_sorted = sorted(movies_meta, key=lambda k: k.get('hash'))
    minted_nft_sorted = sorted(minted_nft_limited, key=lambda k: k.get('cid'))

    # Zip to generate a (A1,A2) => {A} join
    zipped_meta = zip_longest(movies_meta_sorted, minted_nft_sorted)
    zipped_meta_chained = map(lambda x: {**x[0], **x[1]}, zipped_meta)
    movies_meta = map(_sanitize_internals, zipped_meta_chained)
    return jsonify(list(movies_meta))


@cache_.route("/creators", methods=["GET"])
def creators():
    order_by = request.args.get("order", DESCENDING)
    limit = request.args.get("limit", 6)

    # Get current latest minted movies
    aggregation_group = [
        {"$group": {"_id": "$creator", "sum": {"$sum": 1}}},
        {"$limit": limit},
        {"$sort": {"_id": order_by}},
    ]

    recent_minters = manager.aggregated(aggregation_group)
    recent_minters = map(
        lambda x: {"address": x["_id"], "movies": x["sum"]}, recent_minters
    )
    return jsonify(list(recent_minters))
