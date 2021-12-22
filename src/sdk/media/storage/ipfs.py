import typing

import docker
import json
from src.sdk.constants import IPFS_CONTAINER

ipfs = "ipfs"


def get_container():
    client = docker.from_env()
    return client.containers.get(IPFS_CONTAINER)


def exec_command(cmd, *args) -> typing.Union[dict, str]:
    """
    Send commands execution to ipfs node
    :param cmd: please provide path uri scheme eg. /pin/ls/
    based on http://docs.ipfs.io.ipns.localhost:8080/reference/cli/
    """
    container = get_container()
    cmd = " ".join(cmd.split("/"))  # Parse path to commands
    arg_list = " ".join(args)

    _, output = container.exec_run(f"{ipfs} {cmd} {arg_list} --enc=json")
    # If not result just keep object output standard
    if not output:
        return {}

    try:
        json_to_dict = json.loads(output)
        return json_to_dict
    except json.decoder.JSONDecodeError:
        return output.decode("utf-8")


def dag_get(cid, *args):
    """
    Proxy dag get command to node
    http://docs.ipfs.io.ipns.localhost:8080/reference/cli/#ipfs-dag-get
    :param cid:
    """
    return exec_command("/dag/get", cid)


def get_id():
    output = exec_command("id")
    return output.get("ID")
