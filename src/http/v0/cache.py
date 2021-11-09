from flask import jsonify, request
from src.http.main import app
from src.sdk.cache import minted, ingested, DESCENDING
from src.sdk.media.nft import erc1155_metadata
from src.sdk.scheme.validator import check


def _clean_internals(entry):
    del entry["properties"]["properties"]["hash"]
    del entry["properties"]["properties"]["resource"]
    imdb_code = entry["properties"]["properties"]['imdb_code']
    entry["properties"]["image"] = f"/proxy{entry['properties']['image']}?imdb={imdb_code}"
    return entry


@app.route("/cache/recent", methods=["GET"])
def recent():
    limit = request.args.get("limit", 6)

    # Get current latest minted movies
    minted_nft, _ = minted({}, {"cid": 1, "_id": False})
    meta_data_sorted = minted_nft.sort([("_id", DESCENDING)])
    meta_data_limited = meta_data_sorted.limit(limit)
    mapped_cid = list(map(lambda x: x.get("cid"), meta_data_limited))

    # Get "in-relation" hash from ingested metadata
    # Parse erc1155 metadata
    metadata_for_cid, _ = ingested({"hash": {"$in": mapped_cid}})
    movies_meta = map(erc1155_metadata, check(metadata_for_cid))
    movies_meta = map(_clean_internals, movies_meta)

    return jsonify(list(movies_meta))
