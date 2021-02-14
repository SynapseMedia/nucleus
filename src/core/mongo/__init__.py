from pymongo import MongoClient

MONGO_HOST, MONGO_PORT = ('mongodb', '27017')
# Setup mongo local temp cache
mongo_client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")


def get_dbs(*dbs_list):
    return [mongo_client[db] for db in dbs_list]


__all__ = ['mongo_client', 'get_dbs']
