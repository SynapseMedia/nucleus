import typing

import docker
import json
from src.sdk.constants import IPFS_CONTAINER
from src.sdk.exception import IPFSFailedExecution

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


__all__ = ["get_id", "exec_command", "pin", "dag_get", "get_container"]
