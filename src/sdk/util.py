import os
import json
from pathlib import Path
from src.sdk.scheme.definition.movies import MovieScheme
from .constants import RAW_PATH, PROD_PATH


def read_json(input_file: str) -> dict:
    """
    Create an output json file into output file with data
    :param input_file: File dir
    :return: json dict
    """

    with open(
        input_file,
    ) as f:
        return json.load(f)


def write_json(output: str, data: dict) -> str:
    """
    Create an output json file into output file with data
    :param output: Dir
    :param data: dict to write
    :return: path to file
    """

    with open(output, "w") as f:
        json.dump(data, f, ensure_ascii=False)
    return output


def resolve_root_for(_dir: str, is_prod: bool = True) -> [str, bool]:
    """
    Resolve root dir for PROD or RAW based on param
    :param _dir: the dir to resolve
    :param is_prod: determine how resolved the dir
    :return: tuple with root_dir and path_exists
    """
    root_dir = RAW_PATH if not is_prod else PROD_PATH
    root_dir = "%s/%s" % (root_dir, _dir)
    path_exists = Path(root_dir).exists()
    return root_dir, path_exists


def make_destination_dir(_dir: str) -> str:
    """
    Abstraction to make a dir in OS
    :param _dir: dir to create
    :return: string new created dir
    """
    dirname = os.path.dirname(_dir)
    Path(dirname).mkdir(parents=True, exist_ok=True)
    return dirname


def extract_extension(file: str) -> str:
    """
    Extract file extension
    :param file:
    :return: string extension
    """
    _, file_extension = os.path.splitext(file)
    file_extension = file_extension.replace(".", "")
    return file_extension


def build_dir(movie: MovieScheme) -> str:
    """
    Build current local dir for movie
    :param movie MovieSchema /scheme/definition.py
    :return:
    """
    current_imdb_code = movie.imdb_code
    current_linked_name = getattr(movie, "group_name", None)
    current_dir = current_imdb_code
    if current_linked_name:  # If linked_name add sub-dir
        current_dir = f"{current_linked_name}/{current_imdb_code}"
    return current_dir
