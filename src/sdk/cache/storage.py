
import src.core.cache as cache

from src.core.cache.types import Connection
from .manager import all


@cache.atomic
def freeze(connuid, data):
    """
    Insert and mark entry as updated in raw_db
    :param uid: The entry id
    :param data: data to store
    :return: data dict
    """
    
    

    cursor_db.movies.insert_one(data)
    raw_db.movies.update_one({"imdb_code": uid}, {"$set": {"updated": True}})

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
