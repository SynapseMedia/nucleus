from .ipc import IPC


def call(cmd: str) -> IPC:
    """Spawn subprocess .

    :param cmd: Process to execute
    :return: Inter process communication instance
    """
    return IPC(cmd)
