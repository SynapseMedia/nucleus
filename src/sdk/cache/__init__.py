from pymongo import MongoClient, ASCENDING, DESCENDING
from ..constants import MONGO_HOST, MONGO_PORT, DB_DATE_VERSION, REGEN_MOVIES

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
raw_db, cursor_db, mint_db, bid_db = get_dbs(tmp_db_name, "cursor", "mint", "bid")

# Check for empty db
empty_tmp = raw_db.movies.count() == 0
empty_cursor = cursor_db.movies.count() == 0
empty_mint_db = mint_db.movies.count() == 0
empty_bid_db = bid_db.movies.count() == 0

from . import ingest  # noqa
from . import mint  # noqa
from . import manager  # noqa
from . import bid  # noqa

__all__ = [
    "get_dbs",
    "cursor_db",
    "bid_db",
    "raw_db",
    "mint_db",
    "DESCENDING",
    "ASCENDING",
    "ingest",
    "mint",
    "bid",
    "manager",
]
