import os
from pymongo import MongoClient
from src.core import logger
from datetime import date

# Setup mongo local temp cache
MONGO_HOST, MONGO_PORT = ('mongodb', '27017')
mongo_client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")

DB_DATE_VERSION = date.today().strftime('%Y%m%d')
ROOT_PROJECT = os.getenv('PROJECT_ROOT')
REGEN_MOVIES = os.getenv('REGEN_MOVIES', 'False') == 'True'


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
tmp_db_name = 'witth%s' % DB_DATE_VERSION if REGEN_MOVIES else 'witth'
temp_db, transcode_db, cursor_db = get_dbs(tmp_db_name, 'transcode', 'ipfs')

# Check for empty db
empty_tmp = temp_db.movies.count() == 0
empty_cursor = cursor_db.movies.count() == 0
empty_transcode = transcode_db.movies.count() == 0

# Initialize
logger.info('Setting mongodb')
logger.info("Running %s version in %s directory" % (DB_DATE_VERSION, ROOT_PROJECT))
logger.info('\n')

# An important note about collections (and databases) in MongoDB is that they are created lazily
# https://pymongo.readthedocs.io/en/stable/tutorial.html#making-a-connection-with-mongoclient
__all__ = ['empty_cursor', 'empty_tmp', 'empty_transcode', 'temp_db', 'transcode_db', 'cursor_db', 'get_dbs']
