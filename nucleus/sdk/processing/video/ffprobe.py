import ffmpeg

# Convention for importing types
from nucleus.core.types import JSON, Any, Path
from nucleus.sdk.exceptions import FFProbeError


# TODO add auto_probe feature to encoding step
# TODO set video->0, audio->1 streams methods
def probe(path: Path, **kwargs: Any) -> JSON:
    """Run ffprobe on the specified file and return a JSON representation of the output.

    :param path: The path to probe
    :return: JSON representation of the output
    :raises FFProbeError: If the file path does not exist
    """
    try:
        return JSON(ffmpeg.probe(path, **kwargs))
    except ffmpeg._run.Error as e:
        raise FFProbeError(f'error during ffprobe command call: {str(e)}')


__all__ = ('probe',)
