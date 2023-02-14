import pathlib
import src.core.fs as fs
import src.core.http as http

from src.core.types import URI, Tuple, Directory, Union
from .constants import PROD_PATH, RAW_PATH


def resolve(dir_: Directory, is_prod: bool = True) -> Tuple[Directory, bool]:
    """Resolve dir for media in directory PROD or RAW.

    :param dir_: the dir to resolve
    :param is_prod: determine how resolved the dir
    :return: tuple with root_dir and path_exists
    :rtype: str, bool
    """
    target_path = RAW_PATH if not is_prod else PROD_PATH
    root_dir = Directory("%s/%s" % (target_path, dir_))

    path_exists = fs.exists(root_dir)
    return Directory(root_dir), path_exists


def fetch(route: Union[URI, Directory], output: Directory) -> pathlib.Path:
    """Fetch files from the given route.
    If the file is a local file it copy it to output dir.

    :param route: File route reference
    :param output: Where store the file?
    :return: Directory of stored file
    :rtype: pathlib.Path
    """

    if pathlib.Path(route).is_file():
        source = Directory(route)  # source directory
        out_dir = pathlib.Path(output)
        # Check if output file already exists
        if out_dir.exists():
            return out_dir

        output = fs.copy(source, output)  # copy the file to output
        return pathlib.Path(output)

    return http.download(URI(route), output)
