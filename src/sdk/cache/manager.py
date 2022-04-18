from src.sdk.cache import raw_db, mint_db, cursor_db
from pymongo.errors import BulkWriteError
from ..exception import EmptyCache


def get(db=None, _filter=None, opts=None):
    """
    Return resolved entry
    from cache tmp db
    :param db: tmp_db
    :param _filter:
    :param opts:
    :return: Cursor
    """

    db = db or raw_db
    current_filter = _filter or {}
    return db.movies.find_one(
        current_filter,
        opts
        # no_cursor_timeout=True
    )


def aggregated(db=None, pipeline=None):
    """
    Amplifier function to handle aggregation strategy
    :param db: The db to aggregate
    :param pipeline: Pipeline
    https://docs.mongodb.com/v4.0/reference/method/db.collection.aggregate/
    :return: CommandCursor, count
    """
    db = db or cursor_db
    pipeline = pipeline or dict()
    return db.movies.aggregate(pipeline)


def retrieve(db=None, _filter=None, opts=None):
    """
    Return all resolved entries
    from cache tmp db
    :param db: tmp_db
    :param _filter:
    :param opts:
    :return: Cursor, count
    """

    db = db or raw_db
    current_filter = _filter or {}
    result_set = db.movies.find(
        current_filter,
        opts
        # no_cursor_timeout=True
    ).batch_size(1000)

    # Return set + entries count
    return result_set, result_set.count()


def safe_retrieve(db=None, _filter=None):
    """
    Return all resolved entries with empty check
    :param db: tmp_db
    :param _filter:
    :return: Cursor, count
    :raises: EmptyCache
    """
    result, result_count = retrieve(db, _filter)
    if result_count == 0:  # If not data to fetch
        raise EmptyCache()

    return result, result_count


def flush(db=None, _filter: dict = None):
    """
    Flush db for specified _filter
    :param _filter: filter dict
    """
    return db.movies.delete_many(_filter)


def flush_all():
    """
    Reset old entries and restore
    available entries to process in tmp_db
    :return:
    """
    flush(cursor_db, {})
    flush(mint_db, {})
    raw_db.movies.update_many(
        # Filter processed
        {"updated": True},
        # Mark the processed as pending
        {"$unset": {"updated": None}},
    )


def rewrite(data):
    """
    Just remove old data and replace it with new data in temp db
    :param data:
    """
    try:
        raw_db.movies.delete_many({})  # Clean all
        raw_db.movies.insert_many(data)
    except BulkWriteError:
        pass
