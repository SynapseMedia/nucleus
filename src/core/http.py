import random
import requests
import shutil
import pathlib
import src.core.files as files
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
    files.make(output)

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


def fetch(route: URI, output: Directory) -> pathlib.Path:
    """Fetch files from the given route

    :param route: File route reference
    :param output: Where store the file?
    :return: Directory of stored file
    :rtype: pathlib.Path
    """

    # Resolve root directory for PROD
    path, path_exists = files.resolve(output)

    # path already exists?
    if path_exists:
        logger.log.notice(f"File already exists: {path}")  # type: ignore
        return pathlib.Path(path)

    # Check if route is file path and exists in host to copy it to prod dir
    if pathlib.Path(route).is_file():
        logger.log.notice(f"Copying existing file: {route}")  # type: ignore
        files.make(path)  # make thr path if doesn't exists
        shutil.copy(route, path)  # copy the file to recently created directory
        return pathlib.Path(path)

    return download(route, path)
