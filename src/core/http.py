import requests
import pathlib
import src.core.fs as fs
import src.core.logger as logger
import requests.exceptions as exceptions

from src.core.constants import VALIDATE_SSL
from src.core.types import URI, Directory

# Session keep alive
session = requests.Session()


def download(route: URI, output: Directory) -> pathlib.Path:
    """Download remote media

    :param route: URI
    :param output: Where store it?
    :return: path to file directory recently downloaded
    :rtype: pathlib.Path
    :raises exceptions.HTTPError: if fail requesting download route URI
    """

    # Create if not exist dir
    fs.make(output)

    # Start http session
    response = session.get(
        route,  # Uri to fetch from multimedia
        stream=True,
        timeout=60,
        verify=VALIDATE_SSL,
    )

    # Check status for response
    if response.status_code != requests.codes.ok:
        raise exceptions.HTTPError()

    logger.log.info(f"Trying fetch to: {output}")
    with open(output, "wb") as out:
        for block in response.iter_content(256):
            if not block:
                break
            out.write(block)
        out.close()

    logger.log.success(f"File stored in: {output}")  # type: ignore
    return pathlib.Path(output)
