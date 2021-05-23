import os
import random
import requests
from pathlib import Path
from src.core import Log, logger

VALIDATE_SSL = os.environ.get('VALIDATE_SSL', 'False') == 'True'
ROOT_PATH = os.environ.get('RAW_DIRECTORY')

# Session keep alive
# http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects
_agents = [
    'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
]


def resolve_root_dir(_dir):
    return "%s/%s" % (ROOT_PATH, _dir)


def download_file(uri, _dir) -> str:
    """
    Take from the boring centralized network
    :param uri: Link to file
    :param _dir: Where store the file?
    :return: Directory of stored file
    """
    session = requests.Session()
    directory = resolve_root_dir(_dir)
    dirname = os.path.dirname(directory)
    file_check = Path(directory)

    # already exists?
    if file_check.exists():
        logger.warning(f"{Log.WARNING}File already exists: {directory}{Log.ENDC}")
        return directory

    # Create if not exist dir
    Path(dirname).mkdir(parents=True, exist_ok=True)
    response = session.get(uri, verify=VALIDATE_SSL, stream=True, timeout=60, headers={
        'User-Agent': _agents[random.randint(0, 3)]
    })

    # Check status for response
    if response.status_code == requests.codes.ok:
        logger.warning(f"{Log.WARNING}Trying download to: {directory}{Log.ENDC}")
        with open(directory, "wb") as out:
            for block in response.iter_content(256):
                if not block: break
                out.write(block)
            out.close()

    logger.info(f"{Log.OKGREEN}File stored in: {directory}{Log.ENDC}")
    return directory
