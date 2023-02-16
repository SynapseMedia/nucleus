import src.core.http as http

from src.core.types import URL, Tuple, Union, Path
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


def fetch(route: Union[URL, Path], output: Path) -> Path:
    """Fetch files from the given route.
    If output path exists the file copy is omitted.
    If the route is a local file it copy it to output dir.
    If the route is a URL will try to download it and store it in output.

    :param route: file route reference
    :param output: where store the file?
    :return: directory of stored file
    :rtype: Path
    """

    # if exists omit the process
    if output.exists():
        return output

    # copy the file to output
    if isinstance(route, Path) and route.is_file():
        return route.copy(output)

    # Otherwise try to download the file from URI
    return http.download(URL(route), output)
