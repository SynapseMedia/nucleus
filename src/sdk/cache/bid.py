from src.sdk.cache import bid_db
from src.sdk.cache.manager import retrieve
from datetime import datetime


def freeze(account: str, bid: str, movie: str) -> dict:
    """
    Insert into cache bid for movie
    :param account: Bidder
    :param bid: Bid amount
    :param movie: Movie id
    """
    zipped = {
        "bid": bid,
        "movie": movie,
        "account": account,
        "created_at": datetime.now(),
    }

    bid_db.movies.insert({**zipped})
    return zipped


def frozen(_filter: dict = None, _opts: dict = None):
    """
    Return bids for movie
    :param _filter: filter dic
    :param _opts: opts dic
    :return: Cursor
    """
    return retrieve(bid_db, _filter, _opts)


def flush(_filter: dict = None, _opts: dict = None):
    """
    Flush bids for specified _filter and _opts
    :param _filter: filter dict
    :param _opts: _opts dict

    """
    pass
