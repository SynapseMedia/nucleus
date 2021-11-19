import requests
from ipfshttpclient.exceptions import ErrorResponse
from src.sdk import logger, media
from src.sdk.constants import (
    VALIDATE_SSL,
    PINATA_API_SECRET,
    PINATA_API_KEY,
    PINATA_ENDPOINT,
    PINATA_PSA,
    PINATA_SERVICE,
    PINATA_API_JWT,
    PINATA_PIN_BACKGROUND,
)

# Session keep alive
session = requests.Session()


def _find_service_in_list(service: dict):
    """
    Check if "pinata" is a pin remote service in node
    :param service: Current processed Service dic
    :return: Tuple with value found or tuple with None (None,) || (pinata,)
    """
    return next(
        (
            i["Service"]
            for i in service["RemoteServices"]
            if i["Service"] == PINATA_SERVICE
        ),
        None,
    )


def has_valid_registered_service():
    """
    Check if pinata service is already registered
    :return: False if not registered else True
    """
    ipfs_api_client = media.ingest.ipfs.get_client()
    args = (PINATA_SERVICE, PINATA_PSA, PINATA_API_JWT)
    registered_services = ipfs_api_client.request(
        "/pin/remote/service/ls", args, decoder="json"
    )

    # Map result from registered services and search for "pinata"
    find_registered_service = map(_find_service_in_list, registered_services)
    return PINATA_SERVICE in tuple(filter(None, find_registered_service))


def pin_remote(cid: str, **kwargs):
    """
    Pin cid into edge pinata remote cache
    :param cid: the cid to pin
    :return
    """

    if not has_valid_registered_service():
        register_service()

    try:
        args = (cid,)
        ipfs_api_client = media.ingest.ipfs.get_client()
        kwargs.setdefault(
            "opts", {"service": PINATA_SERVICE, "background": PINATA_PIN_BACKGROUND}
        )
        return ipfs_api_client.request(
            "/pin/remote/add", args, decoder="json", **kwargs
        )
    except ErrorResponse:
        logger.log.warning("Object already pinned to pinata")
        logger.log.warning("Please remove or replace existing pin object")
        logger.log.info("\n")


def register_service():
    """
    Register edge service in ipfs node
    :return: request result according to
    https://docs.ipfs.io/reference/http/api/#api-v0-pin-remote-service-add
    """
    if has_valid_registered_service():
        logger.log.warning("Service already registered")
        return

    ipfs_api_client = media.ingest.ipfs.get_client()
    args = (PINATA_SERVICE, PINATA_PSA, PINATA_API_JWT)
    logger.log.info("Registering pinata service")
    return ipfs_api_client.request("/pin/remote/service/add", args, decoder="json")


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
    return response.status_code == requests.codes.ok and has_valid_registered_service()
