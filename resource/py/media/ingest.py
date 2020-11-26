import ipfshttpclient
import os
import random
import requests
from pathlib import Path

__author__ = 'gmena'
# Session keep alive
# http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects

_agents = [
    'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
]

try:
    ipfs = ipfshttpclient.connect('/dns/ipfs/tcp/5001/http')
    root_path = os.path.dirname(os.path.realpath(__file__))
    print(ipfs.id())
except ipfshttpclient.exceptions.ConnectionError:
    exit(0)


def download_file(uri, _dir):
    """
    Take from the boring centralized network
    :param uri:
    :param _dir:
    :return:
    """
    session = requests.Session()
    directory = "%s/torrents%s" % (root_path, _dir)
    dirname = os.path.dirname(directory)
    file_check = Path(directory)

    # already exists?
    if file_check.is_file():
        print("Existing file: ", directory)
        return directory

    # Create if not exist dir
    Path(dirname).mkdir(parents=True, exist_ok=True)
    response = session.get(uri, verify=True, timeout=60, headers={
        'User-Agent': _agents[random.randint(0, 3)]
    })

    # Check status for response
    if response.status_code == requests.codes.ok:
        # Avoid to re-download
        out = open(directory, "wb")
        for block in response.iter_content(1024):
            if not block: break
            out.write(block)
        out.close()

    print('File stored in:', directory)
    return directory


def ingest_ipfs(uri, _dir):
    """
    Go and conquer the world little child!!
    :param uri:
    :param _dir:
    :return:
    """
    directory = download_file(uri, _dir)
    print('Adding IPFS file:', directory)
    return ipfs.add(directory, pin=True)['Hash']
