from flask import Response, stream_with_context, request
from src.http.main import app
from src.sdk.exception import InvalidRequest
from src.sdk.cache import get, cursor_db
from src.sdk.constants import IPFS_NODE, IPFS_NODE_GATEWAY_PORT
import requests


@app.route("/proxy/<file>", methods=["GET"])
def proxy(file):
    """Get a object id and return assets"""
    imdb_code = request.args.get("imdb", "")
    if not imdb_code:
        raise InvalidRequest()

    local_node_uri = f"{IPFS_NODE}:{IPFS_NODE_GATEWAY_PORT}"
    proxy_movie = get(cursor_db, _filter={"imdb_code": imdb_code})
    # Sanitize URI to request from local IPFS gateway
    file_node_path = f"{local_node_uri}/ipfs/{proxy_movie['hash']}/{file}"
    req = requests.get(file_node_path, stream=True)
    # Proxy response from gateway
    return Response(
        stream_with_context(req.iter_content(chunk_size=1024)),
        content_type=req.headers["content-type"],
    )
