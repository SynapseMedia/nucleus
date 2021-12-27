import sys

import requests

from src.sdk import logger
from src.sdk.media.storage import session
from src.sdk.exception import IPFSFailedExecution
from src.sdk.media.storage.ipfs import exec_command
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


def has_valid_registered_service():
    """
    Check if pinata service is already registered
    :return: False if not registered else True
    """
    registered_services = exec_command("/pin/remote/service/ls")
    registered_services_list = registered_services.get("RemoteServices")
    # Map resulting from registered services and search for "pinata"
    return any(map(lambda i: i["Service"] == PINATA_SERVICE, registered_services_list))


def pin(cid: str):
    """
    Pin cid into edge pinata remote cache
    :param cid: the cid to pin
    :return
    """

    if not has_valid_registered_service():
        register_service()

    try:
        args = (
            cid,
            f"--service={PINATA_SERVICE}",
            f"--background={PINATA_PIN_BACKGROUND}",
        )
        return exec_command("/pin/remote/add", *args)
    except IPFSFailedExecution:
        logger.log.warning(
            "Object already pinned to pinata. Please remove or replace existing pin object"
        )
        sys.stdout.write("\n")


def register_service():
    """
    Register edge service in ipfs node
    :return: request result according to
    https://docs.ipfs.io/reference/http/api/#api-v0-pin-remote-service-add
    """
    if has_valid_registered_service():
        logger.log.warning("Service already registered")
        return

    args = (PINATA_SERVICE, PINATA_PSA, PINATA_API_JWT)
    logger.log.info("Registering pinata service")
    return exec_command("/pin/remote/service/add", *args)


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
