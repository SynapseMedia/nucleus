from flask import jsonify, request, Blueprint
from src.sdk.cache import manager, DESCENDING

creator_ = Blueprint("creator", __name__)


@creator_.route("recent", methods=["GET"])
def creators():
    order_by = request.args.get("order", DESCENDING)
    limit = request.args.get("limit", 6)

    # Get current latest minted movies
    aggregation_group = [
        {"$group": {"_id": "$holder", "sum": {"$sum": 1}}},
        {"$limit": limit},
        {"$sort": {"_id": order_by}},
    ]

    recent_minters = manager.aggregated(aggregation_group)
    recent_minters = map(
        lambda x: {"address": x["_id"], "movies": x["sum"]}, recent_minters
    )
    return jsonify(list(recent_minters))
