from src.core.types import CIDStr, Directory
from .cmd import CLI


def directory(path: Directory) -> CIDStr:
    """Add directory to ipfs
    ref: https://docs.ipfs.io/reference/cli/#ipfs-add

    :param path: Directory to add to IPFS
    :return: The resulting CID
    :rtype: CIDStr
    :raises IPFSFailedExecution: if ipfs cmd execution fail
    """
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
    hash_ = exec().get("output")

    # Cleaned returned cid
    return hash_.strip()
