import os
import errno
import pathlib
import contextlib
from src.core.types import Tuple, Directory, Iterator
from src.core.constants import PROD_PATH, RAW_PATH


@contextlib.contextmanager
def read(_dir: str) -> Iterator[str]:
    """Return file content.

    :param _dir: file path
    :return: file content
    :rtype: str
    :raises FileNotFoundError
    """

    # Lets ensure that the database file exists
    path_exists = exists(_dir)
    if not path_exists:  # Check if path exist if not just pin_cid_list
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), _dir)

    with open(_dir) as _file:
        content = _file.read()
        _file.close()  # don't leak a file descriptor
        yield content


def exists(_dir: Directory) -> bool:
    """Check if a path exists in the given directory

    :param _dir: Directory to check
    :return: True if the path exists
    :rtype: bool
    """
    path_exists = pathlib.Path(_dir).exists()
    return path_exists


def resolve(_dir: Directory, is_prod: bool = True) -> Tuple[Directory, bool]:
    """Resolve root dir for runtime directory PROD or RAW based on 'is_prod' param

    :param _dir: the dir to resolve
    :param is_prod: determine how resolved the dir
    :return: tuple with root_dir and path_exists
    :rtype: str, bool
    """
    target_path = RAW_PATH if not is_prod else PROD_PATH
    root_dir = "%s/%s" % (target_path, _dir)

    path_exists = exists(root_dir)
    return Directory(root_dir), path_exists


def make(_dir: Directory) -> Directory:
    """Abstraction to make a dir in OS

    :param _dir: dir to create
    :return: string new created dir
    :rtype: str
    """
    dirname = os.path.dirname(_dir)
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
