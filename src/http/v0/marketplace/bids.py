from flask import jsonify, request, Blueprint
from src.sdk.cache import bid, DESC
from src.sdk.exception import InvalidRequest

bids_ = Blueprint("bids", __name__)


@bids_.route("recent", methods=["GET"])
def recent():
    uid = request.args.get("id")
    order_by = request.args.get("order", DESC)
    limit = request.args.get("limit", 5)

    bid_list, _ = bid.frozen({"movie": uid}, {"_id": False})
    bid_list = bid_list.sort([("created_at", order_by)]).limit(limit)
    return jsonify(list(bid_list))


@bids_.route("create", methods=["POST"])
def create():

    data = request.get_json()
    from_ = data.get("account")
    bid_ = data.get("bid")
    uid = data.get("id")

    if not uid:
        raise InvalidRequest()

    json = {"movie": uid, "account": from_, "bid": bid_}
    freeze_result = bid.freeze(**json)
    return jsonify(freeze_result)


@bids_.route("flush", methods=["DELETE"])
def flush():

    uid = request.args.get("id")

    if not uid:
        raise InvalidRequest()

    flush_result = bid.flush({"movie": uid})
    return jsonify(flush_result)
