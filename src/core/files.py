import os
import errno
import pathlib
import contextlib

from src.core.types import Tuple, Directory, Iterator
from src.core.constants import PROD_PATH, RAW_PATH


@contextlib.contextmanager
def read(dir_: str) -> Iterator[str]:
    """Return file content.
    If file is not found, exception is raised.

    :param dir_: file path
    :return: file content
    :rtype: str
    :raises FileNotFoundError: if file does not exist
    """

    # Lets ensure that the database file exists
    path_exists = exists(dir_)
    if not path_exists:  # Check if path exist if not raise error
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), dir_)

    with open(dir_, "r") as file:
        content = file.read()
        file.close()  # don't leak a file descriptor
        yield content


def exists(dir_: Directory) -> bool:
    """Check if a path exists in the given directory

    :param dir_: Directory to check
    :return: True if the path exists
    :rtype: bool
    """
    path_exists = pathlib.Path(dir_).exists()
    return path_exists


def resolve(dir_: Directory, is_prod: bool = True) -> Tuple[Directory, bool]:
    """Resolve root dir for runtime directory PROD or RAW based on 'is_prod' param

    :param dir_: the dir to resolve
    :param is_prod: determine how resolved the dir
    :return: tuple with root_dir and path_exists
    :rtype: str, bool
    """
    target_path = RAW_PATH if not is_prod else PROD_PATH
    root_dir = "%s/%s" % (target_path, dir_)

    path_exists = exists(root_dir)
    return Directory(root_dir), path_exists


def make(dir_: Directory) -> Directory:
    """Abstraction to make a dir in OS

    :param dir_: dir to create
    :return: string new created dir
    :rtype: str
    """
    dirname = os.path.dirname(dir_)
    pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
    return Directory(dirname)


def extension(file: Directory) -> str:
    """Extract file extension

    :param file: file path
    :return: extension
    :rtype: str
    """

    _, file_extension = os.path.splitext(file)
    file_extension = file_extension.replace(".", "")
    return file_extension
