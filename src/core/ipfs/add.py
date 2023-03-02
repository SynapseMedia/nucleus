from src.core.types import CID, Path
from .cmd import CLI


def directory(path: Path) -> CID:
    """Add directory to ipfs
    ref: https://docs.ipfs.io/reference/cli/#ipfs-add

    :param path: Directory to add to IPFS
    :return: The resulting CID
    :rtype: CIDStr
    :raises IPFSRuntimeException: if ipfs cmd execution fail
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
    call = CLI("/add", *args)()
    # Cleaned returned cid
    return call.output.strip()
