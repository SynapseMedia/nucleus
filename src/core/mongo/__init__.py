from pymongo import MongoClient

# Setup mongo local temp cache
MONGO_HOST, MONGO_PORT = ('mongodb', '27017')
mongo_client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")


def get_dbs(*dbs_list) -> tuple:
    """
    Mongo db collection initialization from list
    :param dbs_list: The collection list with given name
    :return: Mongo collection list
    """
    return tuple(mongo_client[db] for db in dbs_list)


__all__ = ['mongo_client', 'get_dbs']
