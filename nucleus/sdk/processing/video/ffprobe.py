import ffmpeg  # type: ignore
import nucleus.core.json as json
import nucleus.sdk.exceptions as exceptions

# Convention for importing types
from nucleus.core.types import Path, Any, SimpleNamespace


# TODO add auto_probe feature to encoding step
def probe(path: Path, **kwargs: Any) -> SimpleNamespace:
    """Run ffprobe on the specified file and return a JSON mapped object representation of the output.

    :param path: the path to probe
    :return: simple name space object representation of the output
    :rtype: SimpleNamespace
    :raises ProcessingError: if the file path does not exist
    """
    try:
        raw_probe = ffmpeg.probe(path, **kwargs)  # type: ignore
        return json.to_object(raw_probe)
    except ffmpeg._run.Error as e:  # type: ignore
        raise exceptions.FFProbeError(f"error during ffprobe command call: {str(e)}")


__all__ = ("probe",)
