import random
import requests
import shutil
from pathlib import Path
from .. import util, logger
from ..constants import VALIDATE_SSL


# Session keep alive
session = requests.Session()
# http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects
_agents = [
    "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
]


def download(route, directory):
    """
    Fetch remote media
    :param route: URI
    :param directory: Where store it?
    :return:
    """

    # Create if not exist dir
    util.make_destination_dir(directory)

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
        logger.log.info(f"Trying fetch to: {directory}")
        with open(directory, "wb") as out:
            for block in response.iter_content(256):
                if not block:
                    break
                out.write(block)
            out.close()

        logger.log.success(f"File stored in: {directory}")
        return Path(directory)


def file(_route, _dir) -> Path:
    """
    Take from the boring centralized network
    :param _route: File reference
    :param _dir: Where store the file?
    :return: Directory of stored file
    """

    # Resolve root directory for PROD
    directory, path_exists = util.resolve_root_for(_dir)

    # already exists?
    if path_exists:
        logger.log.notice(f"File already exists: {directory}")
        return Path(directory)

    # Check if route is file to copy it to prod dir
    if Path(_route).is_file():
        logger.log.notice(f"Copying existing file: {_route}")
        util.make_destination_dir(directory)
        shutil.copy(_route, directory)
        return Path(directory)

    return download(_route, directory)
