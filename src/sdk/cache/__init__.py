from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from ..exception import EmptyCache
from ..constants import MONGO_HOST, MONGO_PORT, DB_DATE_VERSION, REGEN_MOVIES

mongo_client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")


def get_dbs(*dbs_list) -> tuple:
    """
    Mongo db collection initialization from list
    :param dbs_list: The collection list with given name
    :return: Mongo collection list
    """
    return tuple(mongo_client[db] for db in dbs_list)


# Initialize db list from name
# tmp_db - keep current resolvers cache
# cursor_db - keep a pointer with already processed cache
tmp_db_name = "witth%s" % DB_DATE_VERSION if REGEN_MOVIES else "witth"
temp_db, cursor_db = get_dbs(tmp_db_name, "ipfs")

# Check for empty db
empty_tmp = temp_db.movies.count() == 0
empty_cursor = cursor_db.movies.count() == 0


def set_ingested_with(_id, data):
    """
    Insert and mark entry as updated in temp_db
    :param _id: The entry id
    :param data: data to store
    :return: data dict
    """

    mongo_client.cursor_db.movies.insert_one(data)
    mongo_client.temp_db.movies.update_one(
        {"imdb_code": _id}, {"$set": {"updated": True}}
    )
    mongo_client.close()
    return data


def retrieve(db=None, _filter=None):
    """
    Return all resolved entries
    from cache tmp db
    :param db: tmp_db
    :param _filter:
    :return: Cursor
    """

    db = db or temp_db
    current_filter = _filter or {}
    result_set = db.movies.find(
        current_filter,
        # no_cursor_timeout=True
    ).batch_size(1000)

    # Return set + entries count
    mongo_client.close()
    return result_set, result_set.count()


def retrieve_with_empty_exception(db=None, _filter=None):
    """
    Return all resolved entries with empty check
    :param db: tmp_db
    :param _filter:
    :return: Cursor
    :raises: EmptyCache
    """
    result, result_count = retrieve(db, _filter)
    if result_count == 0:  # If not data to fetch
        raise EmptyCache()

    return result, result_count


def ingested():
    """
    Return already processed and ingested entries
    :return: Cursor
    """

    return retrieve(cursor_db)


def pending():
    """
    Return pending get ingested entries
    :return: Cursor
    """
    return retrieve(
        _filter={
            # Get only not updated entries
            "updated": {"$exists": False}
        }
    )


def flush():
    """
    Reset old entries and restore
    available entries to process in tmp_db
    :return:
    """

    cursor_db.movies.delete_many({})
    temp_db.movies.update_many({"updated": True}, {"$unset": {"updated": None}})
    mongo_client.close()


def rewrite(data):
    """
    Just remove old data and replace it with new data
    :param data:
    """
    try:
        temp_db.movies.delete_many({})  # Clean all
        temp_db.movies.insert_many(data)
        mongo_client.close()
    except BulkWriteError:
        pass


# An important note about collections (and databases) in MongoDB is that they are created lazily
# https://pymongo.readthedocs.io/en/stable/tutorial.html#making-a-connection-with-mongoclient
__all__ = [
    "empty_cursor",
    "empty_tmp",
    "temp_db",
    "cursor_db",
    "get_dbs",
    "rewrite",
    "retrieve",
    "flush",
    "pending",
    "ingested",
    "set_ingested_with",
    "retrieve_with_empty_exception",
]
