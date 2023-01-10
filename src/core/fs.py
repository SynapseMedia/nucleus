import os
import errno
import pathlib
import contextlib
import shutil

from src.core.types import Directory, Iterator


@contextlib.contextmanager
def read(dir_: Directory) -> Iterator[str]:
    """Return file content.
    If file is not found, exception is raised.

    :param dir_: file path
    :return: file content
    :rtype: Iterator[str]
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
    return pathlib.Path(dir_).exists()


def make(dir_: Directory) -> Directory:
    """Abstraction to make a dir in OS

    :param dir_: dir to create
    :return: string new created dir
    :rtype: str
    """
    dirname = os.path.dirname(dir_)
    pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
    return Directory(dirname)


def copy(origin: Directory, output: Directory) -> Directory:
    """ Copy file from origin to output dir.
    If output directory does'nt exists it will be created.
    
    :param origin: file path
    :param output: destination directory
    :return: new absolute file path
    :type: Directory
    """
    
    make(output)  # make the path if doesn't exists
    path = shutil.copy(origin, output)  # copy the file to recently created directory
    return Directory(path)

def extension(file: Directory) -> str:
    """Extract file extension

    :param file: file path
    :return: extension
    :rtype: str
    """

    _, file_extension = os.path.splitext(file)
    file_extension = file_extension.replace(".", "")
    return file_extension
