from src.core import helper
from src.core import media
from src.core import mongo
import asyncio


async def call_orbit_subprocess(regen=False):
    # Spawn node subprocess
    await asyncio.gather(
        helper.run(f"npm run mpdm {regen and '-- -g' or ''}"),
        helper.run(f"npm run mwz {regen and '-- -g' or ''}")
    )


def init_ingestion(idb, wdb, movies_indexed):
    """
    Start ingestion for each movie
    Request, download and add files to ipfs then save as cache in mongo
    :param idb: Cache ipfs db to hold cursor
    :param wdb: Temp movies db with all movies stored from resources
    :param movies_indexed:
    :return:
    """
    for x in movies_indexed:
        _id = x['_id']  # Current id
        ingested_data = media.ingest_ipfs_metadata(x)
        if 'torrents' not in x:
            continue
        idb.movies.insert_one(ingested_data)
        wdb.movies.update_one({'_id': _id}, {'$set': {'updated': True}})
    movies_indexed.close()


def rewrite_entries(db, data):
    """
    Just remove old data and replace it with new data
    :param db:
    :param data:
    :return:
    """
    db.movies.delete_many({})  # Clean all
    bulk = [mongo.InsertOne(i) for k, i in data.items()]
    db.movies.bulk_write(bulk)
