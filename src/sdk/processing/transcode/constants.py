import os


# Transcode constants
HLS_TIME = 5
HLS_LIST_SIZE = 10

MAX_FAIL_RETRY = 3
MAX_MUXING_QUEUE_SIZE = 9999

OVERWRITE_TRANSCODE = os.getenv("OVERWRITE_TRANSCODE_OUTPUT", "False")
OVERWRITE_TRANSCODE_OUTPUT = OVERWRITE_TRANSCODE == "True"
DEFAULT_NEW_FILENAME = "index.m3u8"

HLS_NEW_FILENAME = "index.m3u8"
DASH_NEW_FILENAME = "index.mpd"
