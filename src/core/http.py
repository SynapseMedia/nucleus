import requests
import requests.exceptions as exceptions

from src.core.constants import VALIDATE_SSL
from src.core.types import URL, Path

# Session keep alive
session = requests.Session()


def download(route: URL, output: Path) -> Path:
    """Download remote media.
    If output does not exists, it will be created.

    :param route: URI
    :param output: Where store it?
    :return: path to file directory recently downloaded
    :rtype: pathlib.Path
    :raises exceptions.HTTPError: if fail requesting download route URI
    """

    # Create if not exist dir
    output.make()

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

    with open(output, "wb") as out:
        for block in response.iter_content(256):
            if not block:
                break
            out.write(block)
        out.close()

    return output
