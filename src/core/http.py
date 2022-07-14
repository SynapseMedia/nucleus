import random
import requests
import shutil
from pathlib import Path

from . import files, logger
from .constants import VALIDATE_SSL
from .types import Directory, URI


# Session keep alive
session = requests.Session()
# http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects
_agents = [
    "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
]


def download(route: URI, output: Directory):
    """Download remote media

    :param route: URI
    :param output: Where store it?
    :return: path to file directory recently downloaded
    :rtype: pathlib.Path
    """

    # Create if not exist dir
    files.make(output)

    # Start http session
    response = session.get(
        route,  # Uri to fetch from multimedia
        verify=VALIDATE_SSL,
        stream=True,
        timeout=60,
        headers={"User-Agent": _agents[random.randint(0, 3)]},
    )

    # Check status for response
    if response.status_code == requests.codes.ok:
        logger.log.info(f"Trying fetch to: {output}")
        with open(output, "wb") as out:
            for block in response.iter_content(256):
                if not block:
                    break
                out.write(block)
            out.close()

        logger.log.success(f"File stored in: {output}")  # type: ignore
        return Path(output)


def fetch(route: URI, output: Directory):
    """Fetch files from the given route

    :param route: File route reference
    :param output: Where store the file?
    :return: Directory of stored file
    :rtype: pathlib.Path
    """

    # Resolve root directory for PROD
    path, path_exists = files.resolve(output)

    # already exists?
    if path_exists:
        logger.log.notice(f"File already exists: {path}")  # type: ignore
        return Path(path)

    # Check if route is file to copy it to prod dir
    if Path(route).is_file():
        logger.log.notice(f"Copying existing file: {route}")  # type: ignore
        files.make(path)
        shutil.copy(route, path)
        return Path(path)

    return download(route, path)
