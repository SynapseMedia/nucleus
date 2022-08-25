import random
import requests
import shutil
import pathlib
import src.core.files as files
import src.core.logger as logger

from src.core.constants import VALIDATE_SSL
from src.core.types import URI, Directory

# Session keep alive
session = requests.Session()
# http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects
agents = [
    "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
]


def download(route: URI, output: Directory) -> pathlib.Path:
    """Download remote media

    :param route: URI
    :param output: Where store it?
    :return: path to file directory recently downloaded
    :rtype: pathlib.Path
    :raises InvalidImageSize
    """

    # Create if not exist dir
    files.make(output)

    # Start http session
    response = session.get(
        route,  # Uri to fetch from multimedia
        stream=True,
        timeout=60,
        verify=VALIDATE_SSL,
        headers={"User-Agent": agents[random.randint(0, 3)]},
    )

    # Check status for response
    if response.status_code != requests.codes.ok:
        raise requests.exceptions.HTTPError()

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
