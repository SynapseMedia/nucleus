from src.sdk.cache import cursor_db, raw_db
from src.sdk.cache.manager import retrieve


def freeze(_id, data):
    """
    Insert and mark entry as updated in raw_db
    :param _id: The entry id
    :param data: data to store
    :return: data dict
    """

    cursor_db.movies.insert_one(data)
    raw_db.movies.update_one({"imdb_code": _id}, {"$set": {"updated": True}})

    return data


def frozen(_filter: dict = None, _opts: dict = None):
    """
    Return already processed and ingested entries
    :param _filter: filter dic
    :param _opts: opts dic
    :return: Cursor, count
    """

    return retrieve(cursor_db, _filter, _opts)


def pending():
    """
    Return pending get ingested entries
    :return: Cursor, count
    """
    return retrieve(
        _filter={
            # Get only not updated entries
            "updated": {"$exists": False}
        }
    )
