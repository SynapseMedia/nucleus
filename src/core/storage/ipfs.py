
import os
import errno
import docker
import json

from ..constants import IPFS_CONTAINER
from ..exception import IPFSFailedExecution
from ..util import resolve_root_for

ipfs = "ipfs"


def get_container():
    client = docker.from_env()
    return client.containers.get(IPFS_CONTAINER)


def exec_command(cmd, *args):
    """Send commands execution to ipfs node
    
    :param cmd: please provide path uri scheme eg. /pin/ls/
    based on http://docs.ipfs.io.ipns.localhost:8080/reference/cli/
    """
    container = get_container()
    cmd = " ".join(cmd.split("/"))  # Parse path to commands
    arg_list = " ".join(args)

    # Command execution delegated to docker ipfs
    code, output = container.exec_run(f"{ipfs} {cmd} {arg_list} --enc=json")

    if code > 0:
        """
        The CLI will exit with one of the following values:

        0     Successful execution.
        1     Failed executions.
        """
        raise IPFSFailedExecution(output.decode("utf-8"))

    # If not result just keep object output standard
    if not output:
        return {}

    try:
        json_to_dict = json.loads(output)
        return json_to_dict
    except json.decoder.JSONDecodeError:
        return output.decode("utf-8")


def pin(cid):
    """
    Pin cid into local node
    :param cid: the cid to pin
    :return
    """

    return exec_command("/pin/add/", cid)


def dag_get(cid):
    """
    Retrieve dag information from cid
    Proxy dag get command to node
    http://docs.ipfs.io.ipns.localhost:8080/reference/cli/#ipfs-dag-get
    :param cid:
    """
    return exec_command("/dag/get", cid)


def get_id():
    output = exec_command("id")
    return output.get("ID")


def add_dir(_dir: str):
    """Add directory to ipfs

    :param _dir: Directory to add to IPFS
    :return: The resulting CID
    """
    directory, path_exists = resolve_root_for(_dir)

    if not path_exists:  # Check if path exist if not just pin_cid_list
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), directory)

    # avoid pin by default /reference/http/api/#http-commands
    # hash needed to encode to bytes16 and hex
    args = (
        directory,
        "--recursive",
        "--quieter",
        "--cid-version=1",
        "--pin=false",
        "--hash=blake2b-208",
    )

    _hash = exec_command("add", *args)
    return _hash.strip()


__all__ = ["get_id", "exec_command", "pin", "dag_get", "get_container"]
