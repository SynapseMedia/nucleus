import json

# Convention for importing types
from src.core.types import Path, Any, SimpleNamespace, JSON


def read(input_file: Path) -> JSON:
    """Create an output json file into output file with data

    :param input_file: File dir
    :return: json dict
    :rtype: JSON
    """
    with open(input_file) as f:
        return json.load(f)


def write(output: Path, data: JSON) -> Path:
    """Create an output json file into output file with data

    :param output: directory to store file
    :param data: dict to write
    :return: path to file
    :rtype: Directory
    """
    with open(output, "w") as f:
        json.dump(data, f, ensure_ascii=False)
    return Path(output)


def to_object(data: JSON) -> Any:
    """Recursively convert a nested JSON as SimpleNamespace object

    :param data: JSON to recursively convert
    :return: SimpleNamespace object mirroring JSON representation
    :rtype: SimpleNamespace
    """

    if type(data) is list:
        # if is a list recursive parse the entries
        return list(map(to_object, data))

    if type(data) is dict:
        # if is a dict recursive parse
        container = SimpleNamespace()
        for k, v in data.items():
            setattr(container, k, to_object(v))
        return container

    return data
