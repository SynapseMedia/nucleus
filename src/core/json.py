import json
# Convention for importing types
from src.core.types import Directory, Any, Dict


def read(input_file: Directory) -> Dict[Any, Any]:
    """Create an output json file into output file with data

    :param input_file: File dir
    :return: json dict
    :rtype: dict
    """
    with open(input_file) as f:
        return json.load(f)


def write(output: str, data: Dict[Any, Any]) -> Directory:
    """Create an output json file into output file with data

    :param output: directory to store file
    :param data: dict to write
    :return: path to file
    :rtype: str
    """
    with open(output, "w") as f:
        json.dump(data, f, ensure_ascii=False)
    return Directory(output)
