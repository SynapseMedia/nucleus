import sys
import datetime


def progress(_, duration: int, time_: int, time_left: int):
    """Render tqdm progress bar."""
    sys.stdout.flush()
    per = round(time_ / duration * 100)
    sys.stdout.write(
        "\rTranscoding...(%s%%) %s left [%s%s]"
        % (
            per,
            datetime.timedelta(seconds=int(time_left)),
            "#" * per,
            "-" * (100 - per),
        )
    )
