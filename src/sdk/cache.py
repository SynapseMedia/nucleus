from pymongo.errors import BulkWriteError


def retrieve(db=None, _filter=None):
    """
    Return all resolved entries
    from cache tmp db
    :param db: tmp_db
    :param _filter:
    :return: Cursor
    """
    from . import mongo
    db = db or mongo.temp_db
    current_filter = _filter or {}
    result_set = db.movies.find(
        current_filter,
        # no_cursor_timeout=True
    ).batch_size(1000)

    # Return set + entries count
    mongo.mongo_client.close()
    return result_set, result_set.count()


def set_updated_with(_id, data):
    """
    Insert and mark entry as updated in temp_db
    :param _id: The entry id
    :param data: data to store
    :return: data dict
    """
    from . import mongo
    mongo.cursor_db.movies.insert_one(data)
    mongo.temp_db.movies.update_one({"imdb_code": _id}, {"$set": {"updated": True}})
    mongo.mongo_client.close()
    return data


def retrieve_updated():
    """
    Return already processed and ingested entries
    :return: Cursor
    """
    return retrieve(_filter={
        # Get only not updated entries
        "updated": {"$exists": False}
    })


def flush():
    """
    Reset old entries and restore
    available entries to process in tmp_db
    :return:
    """
    from . import mongo
    mongo.cursor_db.movies.delete_many({})
    mongo.temp_db.movies.update_many({"updated": True}, {"$unset": {"updated": None}})
    mongo.mongo_client.close()


def rewrite(data):
    """
    Just remove old data and replace it with new data
    :param data:
    """
    try:
        from . import mongo
        mongo.temp_db.movies.delete_many({})  # Clean all
        mongo.temp_db.movies.insert_many(data)
        mongo.mongo_client.close()
    except BulkWriteError:
        pass
