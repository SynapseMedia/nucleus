from src.sdk.cache import mint_db
from src.sdk.cache.manager import retrieve
from src.sdk.web3.crypto import cid_to_uint256
from datetime import datetime


def freeze(tx: str, to: str, cid_list: list) -> list:
    """
    Insert into cache already minted entries
    :param tx: Transaction hash
    :param to: Owner
    :param cid_list: List of cid minted to cache
    """
    zipped = [
        {
            "tx": tx,  # transaction hash
            "holder": to,  # owner
            "cid": x,  # cid
            "id": str(cid_to_uint256(x)),  # uint256 id
            "created_at": datetime.now(),
        }
        for x in cid_list
    ]

    mint_db.movies.insert_many(zipped)
    return cid_list


def frozen(_filter: dict = None, _opts: dict = None):
    """
    Return already processed and `minted cid` entries
    :param _filter: filter dic
    :param _opts: opts dic
    :return: Cursor
    """
    return retrieve(mint_db, _filter, _opts)
