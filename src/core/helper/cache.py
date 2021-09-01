from pymongo.errors import BulkWriteError


def retrieve(db, _filter=None):
    """
    Return all resolved entries
    from cache tmp db
    :param db: tmp_db
    :param _filter:
    :return:
    """
    current_filter = _filter or {}
    return db.movies.find(current_filter, no_cursor_timeout=True).batch_size(1000)


def flush_ipfs(cursor_db, tmp_db):
    """
    Reset old entries and restore
    available entries to process in tmp_db
    :param cursor_db:
    :param tmp_db:
    :return:
    """

    cursor_db.movies.delete_many({})
    tmp_db.movies.update_many({"updated": True}, {"$unset": {"updated": None}})


def rewrite(db, data):
    """
    Just remove old data and replace it with new data
    :param db:
    :param data:
    """
    try:
        db.movies.delete_many({})  # Clean all
        db.movies.insert_many(data)
    except BulkWriteError:
        pass
