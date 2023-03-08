# ref:
# https://developer.apple.com/documentation/http_live_streaming/http_live_streaming_hls_authoring_specification_for_apple_devices

# Transcode constants
HLS_TIME = 10
HLS_CODEC = "libx265"
HLS_LIST_SIZE = 0
HLS_TAG_VIDEO_FORMAT = "hvc1"
HLS_CODEC_PARAMS = "lossless=1"
HLS_PLAYLIST_TYPE = "vod"


DEFAULT_AUDIO_CODEC = "aac"
# apple recommends 32-160 kb/s
DEFAULT_VIDEO_BITRATE = "128k"
# The range of the CRF scale is 0–51, where 0 is lossless (higher quality)
DEFAULT_CRF = 0
# The preset determines compression efficiency and therefore affects encoding speed
# This option itemizes a range of choices from veryfast (best speed) to
# veryslow (best quality).
DEFAULT_PRESET = "slow"
# keyframes minimum every 100 frames
DEFAULT_KEY_MIN = 100
# maximum amount of GOP size, maximum every 100 frames there will be a
# keyframe, together with -keyint_min this gives a keyframe every 100
# frames
DEFAULT_GOP = 100
# ffmpeg has scene detection. 0 (stands for false)
DEFAULT_SC_THRESHOLD = 0
