from src.sdk.cache import bid_db
from src.sdk.cache.manager import retrieve
from datetime import datetime


def freeze(bid: str, movie_id: str) -> str:
    """
    Insert into cache bid for movie
    :param bid: Bid amount
    :param movie_id: Movie
    """
    zipped = {
        "bid": bid,
        "movie": movie_id,
        "created_at": datetime.now()
    }

    bid_db.movies.insert(zipped)
    return movie_id


def frozen(_filter: dict = None, _opts: dict = None):
    """
    Return bids for movie
    :param _filter: filter dic
    :param _opts: opts dic
    :return: Cursor
    """
    return retrieve(bid_db, _filter, _opts)
