import time
import ipfshttpclient
import requests

from src.sdk.constants import (
    TIMEOUT_REQUEST,
    RECURSIVE_SLEEP_REQUEST,
)

__author__ = "gmena"

# Session keep alive
session = requests.Session()
ipfs = None


def start_node():
    from src.sdk import logger

    try:
        logger.log.notice("Starting node")
        ipfs_node = ipfshttpclient.connect(
            "/dns/ipfs/tcp/5001/http", session=True, timeout=TIMEOUT_REQUEST
        )
        logger.log.info(f"Node running {ipfs_node.id().get('ID')}")
        logger.log.info("\n")
        return ipfs_node
    except ipfshttpclient.exceptions.ConnectionError:
        logger.log.notice("Waiting for node active")
        time.sleep(RECURSIVE_SLEEP_REQUEST)
        return start_node()


from . import remote  # noqa
from . import ingest  # noqa


def init():
    """
    Setup init node and share it with modules
    """
    ipfs_node = start_node()
    remote.ipfs = ipfs_node  # noqa
    ingest.ipfs = ipfs_node  # noqa


__all__ = ["remote", "ingest"]
