import ffmpeg  # type: ignore

# Convention for importing types
from nucleus.core.types import Path, Any, SimpleNamespace
from nucleus.sdk.exceptions import FFProbeError


def _to_object(data: Any) -> Any:
    """Recursively convert a nested JSON as SimpleNamespace object

    :return: SimpleNamespace object mirroring JSON representation
    :rtype: SimpleNamespace
    """

    # if is a list recursive parse the entries
    if isinstance(data, list):
        return list(map(_to_object, data))

    # if is a dict recursive parse
    if isinstance(data, dict):
        container = SimpleNamespace()
        for k, v in data.items():
            setattr(container, k, _to_object(v))
        return container

    return data


# TODO add auto_probe feature to encoding step
# TODO set video->0, audio->1 streams methods
def probe(path: Path, **kwargs: Any) -> SimpleNamespace:
    """Run ffprobe on the specified file and return a JSON mapped object representation of the output.

    :param path: the path to probe
    :return: simple name space object representation of the output
    :rtype: SimpleNamespace
    :raises FFProbeError: if the file path does not exist
    """
    try:
        raw_probe = ffmpeg.probe(path, **kwargs)  # type: ignore
        return _to_object(raw_probe)
    except ffmpeg._run.Error as e:  # type: ignore
        raise FFProbeError(f"error during ffprobe command call: {str(e)}")


__all__ = ("probe",)
