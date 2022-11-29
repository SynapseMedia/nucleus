import shutil
import pathlib
import src.core.fs as fs
import src.core.http as http
import src.core.logger as logger

from src.core.types import URI, Tuple, Directory
from .constants import PROD_PATH, RAW_PATH


def resolve(dir_: Directory, is_prod: bool = True) -> Tuple[Directory, bool]:
    """Resolve dir for media in directory PROD or RAW.

    :param dir_: the dir to resolve
    :param is_prod: determine how resolved the dir
    :return: tuple with root_dir and path_exists
    :rtype: str, bool
    """
    target_path = RAW_PATH if not is_prod else PROD_PATH
    root_dir = "%s/%s" % (target_path, dir_)

    path_exists = fs.exists(root_dir)
    return Directory(root_dir), path_exists


def fetch(route: URI, output: Directory) -> pathlib.Path:
    """Fetch files from the given route.
    If a file already exists omit the download when a URL is provided.
    If the file is a local file make a copy to output dir.

    :param route: File route reference
    :param output: Where store the file?
    :return: Directory of stored file
    :rtype: pathlib.Path
    """

    # path already exists?
    if pathlib.Path(output).exists():
        logger.log.notice(f"File already exists: {output}")  # type: ignore
        return pathlib.Path(output)

    # Check if route is file path and exists in host to copy it to prod dir
    if pathlib.Path(route).is_file():
        logger.log.notice(f"Copying existing file: {route}")  # type: ignore
        fs.make(output)  # make thr path if doesn't exists
        shutil.copy(route, output)  # copy the file to recently created directory
        return pathlib.Path(output)

    return http.download(route, output)
