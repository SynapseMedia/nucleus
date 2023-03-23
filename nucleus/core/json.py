import json

# Convention for importing types
from nucleus.core.types import Path, Any, SimpleNamespace, JSON


def read(input_file: Path) -> JSON:
    """Create an output json file into output file with data

    :param input_file: File dir
    :return: json dict
    :rtype: JSON
    """
    raw = input_file.read_text()
    return json.loads(raw)


def write(output: Path, data: JSON) -> Path:
    """Create an output json file into output file with data

    :param output: directory to store file
    :param data: dict to write
    :return: path to file
    :rtype: Directory
    """
    json_string = json.dumps(data, ensure_ascii=False)
    output.write_text(json_string)
    return output


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
