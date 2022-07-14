import os
import pathlib

from src.core.types import Tuple, Directory
from src.core.constants import PROD_PATH, RAW_PATH


def resolve(_dir: Directory, is_prod: bool = True) -> Tuple[Directory, bool]:
    """Resolve root dir for PROD or RAW based on 'is_prod' param

    :param _dir: the dir to resolve
    :param is_prod: determine how resolved the dir
    :return: tuple with root_dir and path_exists
    :rtype: str, bool
    """
    target_path = RAW_PATH if not is_prod else PROD_PATH
    root_dir = "%s/%s" % (target_path, _dir)

    path_exists = pathlib.Path(root_dir).exists()
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
