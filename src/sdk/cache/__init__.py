from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import BulkWriteError
from ..exception import EmptyCache
from ..constants import MONGO_HOST, MONGO_PORT, DB_DATE_VERSION, REGEN_MOVIES
from . import pinata
ASCENDING = ASCENDING
DESCENDING = DESCENDING

# An important note about collections (and databases) in MongoDB is that they are created lazily
# https://pymongo.readthedocs.io/en/stable/tutorial.html#making-a-connection-with-mongoclient
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
temp_db, cursor_db, mint_db = get_dbs(tmp_db_name, "ipfs", "mint")

# Check for empty db
empty_tmp = temp_db.movies.count() == 0
empty_cursor = cursor_db.movies.count() == 0
empty_mint_db = mint_db.movies.count() == 0


def fetch(db=None, _filter=None, opts=None):
    """
    Return resolved entry
    from cache tmp db
    :param db: tmp_db
    :param _filter:
    :param opts:
    :return: Cursor
    """

    db = db or temp_db
    current_filter = _filter or {}
    return db.movies.find_one(
        current_filter,
        opts
        # no_cursor_timeout=True
    )


def retrieve(db=None, _filter=None, opts=None):
    """
    Return all resolved entries
    from cache tmp db
    :param db: tmp_db
    :param _filter:
    :param opts:
    :return: Cursor
    """

    db = db or temp_db
    current_filter = _filter or {}
    result_set = db.movies.find(
        current_filter,
        opts
        # no_cursor_timeout=True
    ).batch_size(1000)

    # Return set + entries count
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


def set_ingested_with(_id, data):
    """
    Insert and mark entry as updated in temp_db
    :param _id: The entry id
    :param data: data to store
    :return: data dict
    """

    cursor_db.movies.insert_one(data)
    temp_db.movies.update_one({"imdb_code": _id}, {"$set": {"updated": True}})

    return data


def ingested(_filter: dict = None, _opts: dict = None):
    """
    Return already processed and ingested entries
    :return: Cursor
    """

    return retrieve(cursor_db, _filter, _opts)


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
    mint_db.movies.delete_many({})
    temp_db.movies.update_many(
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
        temp_db.movies.delete_many({})  # Clean all
        temp_db.movies.insert_many(data)
    except BulkWriteError:
        pass


def mint(tx: str, to: str, data: list) -> list:
    """
    Insert into cache already minted entries
    """
    zipped = [{"tx": tx, "creator": to, "cid": x} for x in data]
    mint_db.movies.insert_many(zipped)
    return data


def minted(_filter: dict = None, _opts: dict = None):
    """
    Return already processed and minted entries
    :return: Cursor
    """
    return retrieve(mint_db, _filter, _opts)


__all__ = [
    "get_dbs",
    "rewrite",
    "retrieve",
    "flush",
    "pending",
    "ingested",
    "set_ingested_with",
    "retrieve_with_empty_exception",
    "mint",
    "minted",
    "empty_mint_db",
    "pinata",
    "fetch"
]
