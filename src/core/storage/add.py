import errno
import os

from ..types import CIDStr, Directory
from ..files import resolve
from . import CLI

def directory(path: Directory) -> CIDStr:
    """Add directory to ipfs
    ref: https://docs.ipfs.io/reference/cli/#ipfs-add
    
    :param _dir: Directory to add to IPFS
    :return: The resulting CID
    :rtype: CIDStr
    :raises IPFSFailedExecution
    """
    path, path_exists = resolve(path)

    if not path_exists:  # Check if path exist if not just pin_cid_list
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    # no pin by default
    # blake2b-208 hash func to encode to bytes16 and hex
    args = (
        path,
        "--recursive",
        "--quieter",
        "--cid-version=1",
        "--pin=false",
        "--hash=blake2b-208",
    )
    
    # Exec command and get output
    exec = CLI("/add", *args)
    _hash = exec().get("output")
    
    # Cleaned returned cid
    return _hash.strip()
