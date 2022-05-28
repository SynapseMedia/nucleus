import os
import json
from pathlib import Path
from .types import Directory
from typing import Dict, Any, Tuple
from .constants import RAW_PATH, PROD_PATH


def read_json(input_file: Directory) -> Dict[Any, Any]:
    """Create an output json file into output file with data

    :param input_file: File dir
    :return: json dict
    :rtype: dict
    """
    with open(
        input_file,
    ) as f:
        return json.load(f)


def write_json(output: str, data: Dict[Any, Any]) -> Directory:
    """Create an output json file into output file with data

    :param output: directory to store file
    :param data: dict to write
    :return: path to file
    :rtype: str
    """
    with open(output, "w") as f:
        json.dump(data, f, ensure_ascii=False)
    return Directory(output)


def resolve_root_for(_dir: Directory, is_prod: bool = True) -> Tuple[Directory, bool]:
    """Resolve root dir for PROD or RAW based on param

    :param _dir: the dir to resolve
    :param is_prod: determine how resolved the dir
    :return: tuple with root_dir and path_exists
    :rtype: str, bool
    """
    root_dir = RAW_PATH if not is_prod else PROD_PATH
    root_dir = "%s/%s" % (root_dir, _dir)
    path_exists = Path(root_dir).exists()
    return Directory(root_dir), path_exists


def make_destination_dir(_dir: Directory) -> Directory:
    """Abstraction to make a dir in OS

    :param _dir: dir to create
    :return: string new created dir
    :rtype: str
    """
    dirname = os.path.dirname(_dir)
    Path(dirname).mkdir(parents=True, exist_ok=True)
    return Directory(dirname)


def extract_extension(file: Directory) -> str:
    """Extract file extension

    :param file: file path
    :return: extension
    :rtype: str
    """
    _, file_extension = os.path.splitext(file)
    file_extension = file_extension.replace(".", "")
    return file_extension
