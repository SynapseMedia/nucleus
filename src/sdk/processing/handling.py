import src.core.http as http

from src.core.types import URI, Tuple, Union, Path
from .constants import PROD_PATH, RAW_PATH


def resolve(dir_: Path, is_prod: bool = True) -> Tuple[Path, bool]:
    """Resolve dir for media in directory PROD or RAW.

    :param dir_: the dir to resolve
    :param is_prod: determine how resolved the dir
    :return: tuple with root_dir and path_exists
    :rtype: str, bool
    """
    target_path = RAW_PATH if not is_prod else PROD_PATH
    root_dir = Path("%s/%s" % (target_path, dir_))
    return Path(root_dir), root_dir.exists()


def fetch(route: Union[URI, Path], output: Path) -> Path:
    """Fetch files from the given route.
    If the file is a local file it copy it to output dir.

    :param route: File route reference
    :param output: Where store the file?
    :return: Directory of stored file
    :rtype: pathlib.Path
    """

    if Path(route).is_file():
        source = Path(route)  # source directory
        # Check if output file already exists
        if output.exists():
            return output

        output = source.copy(output)  # copy the file to output
        return Path(output)

    return http.download(URI(route), output)
