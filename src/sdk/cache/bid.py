from src.sdk.cache import bid_db
from src.sdk.cache.manager import retrieve
from datetime import datetime


def freeze(account: str, bid: str, uid: str) -> dict:
    """
    Insert into cache bid for movie
    :param account: Bidder
    :param bid: Bid amount
    :param uid: Movie id
    """
    zipped = {
        "bid": bid,
        "account": account,
        "movie": uid,
        "created_at": datetime.now(),
    }

    bid_db.movies.insert(zipped)
    return zipped


def frozen(_filter: dict = None, _opts: dict = None):
    """
    Return bids for movie
    :param _filter: filter dic
    :param _opts: opts dic
    :return: Cursor
    """
    return retrieve(bid_db, _filter, _opts)
