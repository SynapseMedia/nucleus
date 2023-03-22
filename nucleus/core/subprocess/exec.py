from .ipc import IPC


def call(cmd: str) -> IPC:
    """Spawn subprocess .

    :param cmd: process to execute
    :return: inter process communication instance
    :rtype: IPC
    """
    return IPC(cmd)
