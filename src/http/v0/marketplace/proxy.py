from flask import Response, stream_with_context, Blueprint, request
from bson.objectid import ObjectId
from src.sdk.exception import InvalidRequest
from src.sdk.cache import manager, cursor_db
from src.sdk.constants import IPFS_NODE, IPFS_NODE_GATEWAY_PORT
import requests

proxy_ = Blueprint("proxy", __name__)


@proxy_.route("/<uid>", methods=["GET"])
def proxy(uid):
    """Get an object id and return assets"""
    if not uid:
        raise InvalidRequest()
    file = request.args.get("arg")
    local_node_uri = f"{IPFS_NODE}:{IPFS_NODE_GATEWAY_PORT}"
    proxy_movie = manager.get(cursor_db, _filter={"_id": ObjectId(uid)})

    # Sanitize URI to request from local IPFS gateway
    file_node_path = f"{local_node_uri}/ipfs/{proxy_movie['hash']}/{file}"
    req = requests.get(file_node_path, stream=True)
    # Proxy response from gateway
    return Response(
        stream_with_context(req.iter_content(chunk_size=1024)),
        content_type=req.headers["content-type"],
    )
