import sys
import requests

from . import session
from src.core import logger
from src.core.storage import ipfs
from src.core.exception import IPFSFailedExecution
from src.core.constants import (
    VALIDATE_SSL,
    PINATA_API_SECRET,
    PINATA_API_KEY,
    PINATA_ENDPOINT,
    PINATA_PSA,
    PINATA_SERVICE,
    PINATA_API_JWT,
)


def has_valid_registered_service(service: str):
    """
    Check if pinata service is already registered
    :param service: service name to check if registered
    :return: False if not registered else True
    """
    registered_services_list = ipfs.services()
    # Map resulting from registered services and search for "pinata"
    return any(map(lambda i: i["Service"] == service, registered_services_list))


def pin(cid: str, service: str = PINATA_SERVICE):
    """
    Pin cid into edge pinata remote cache
    :param cid: the cid to pin
    :return
    """

    if not has_valid_registered_service(service):
        raise IPFSFailedExecution("Service %s is not registered", service)

    try:
        ipfs.pin_remote(cid)
    except IPFSFailedExecution:
        logger.log.warning("Object already pinned to pinata")
        sys.stdout.write("\n")


def flush(limit=1000):
    """Flush pinned entries from edge

    :param limit: How many entries to flush?
    """
    pinned = pin_ls(limit)  # Get current pin list from edge service
    logger.log.info(f"Flushing {pinned.get('count')} from edge")

    for _pin in pinned.get("results"):
        _pinned = _pin.get("pin")
        _cid = _pinned.get("cid")

        if unpin(_cid):
            logger.log.info(f"Pin {_cid} removed from edge")
            continue
        logger.log.error(f"Fail trying to remove pin for {_cid}")


def register_service(service: str, endpoint: str, key: str):
    """Register edge service in ipfs node
    https://docs.ipfs.io/reference/http/api/#api-v0-pin-remote-service-add

    @params service: service name
    @params endpoint: service endpoint
    @params key: service jwt
    @return: ipfs execution output
    @rtype: str
    """
    if has_valid_registered_service(service):
        logger.log.warning("Service already registered")
        return

    logger.log.info("Registering pinata service")
    return ipfs.register_service(service, endpoint, key)


def unpin(cid):
    """
    Unpin pinata pinned cid
    :param cid:
    :return boolean: True if unpinned success else False
    """
    response = session.delete(
        f"{PINATA_ENDPOINT}/pinning/unpin/{cid}",
        verify=VALIDATE_SSL,
        headers={
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_API_SECRET,
        },
    )

    return response.ok


def pin_ls(limit=1000):
    """
    Request pinata pinned entries
    :param limit:
    :return: {result: [], count: int}
    """
    response = session.get(
        f"{PINATA_PSA}/pins?limit={limit}",
        verify=VALIDATE_SSL,
        headers={"Authorization": f"Bearer {PINATA_API_JWT}"},
    )

    return response.json()


def check_status():
    """
    Ping request to check for valid auth
    for pinata service
    :return: True if active service else False
    """
    # Start http session
    response = session.get(
        f"{PINATA_ENDPOINT}/data/testAuthentication",
        verify=VALIDATE_SSL,
        headers={
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_API_SECRET,
        },
    )

    # Check status for response
    valid_response_code = response.status_code == requests.codes.ok
    return valid_response_code and has_valid_registered_service()
