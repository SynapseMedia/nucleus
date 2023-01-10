import json

# Convention for importing types
from src.core.types import Directory, Raw


def read(input_file: Directory) -> Raw:
    """Create an output json file into output file with data

    :param input_file: File dir
    :return: json dict
    :rtype: Raw
    """
    with open(input_file) as f:
        return json.load(f)


def write(output: Directory, data: Raw) -> Directory:
    """Create an output json file into output file with data

    :param output: directory to store file
    :param data: dict to write
    :return: path to file
    :rtype: Directory
    """
    with open(output, "w") as f:
        json.dump(data, f, ensure_ascii=False)
    return Directory(output)
