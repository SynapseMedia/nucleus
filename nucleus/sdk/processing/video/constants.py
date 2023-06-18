# HLS default constants
# https://developer.apple.com/documentation/http-live-streaming/hls-authoring-specification-for-apple-devices
HLS_TIME = 10
HLS_LIST_SIZE = 0
HLS_TAG_VIDEO_FORMAT = 'hvc1'
HLS_PLAYLIST_TYPE = 'vod'


DEFAULT_AUDIO_CODEC = 'aac'
# The range of the CRF scale is 0–51, where 0 is lossless (higher quality)
DEFAULT_CRF = 0
# The preset determines compression efficiency and therefore affects encoding speed
# This option itemizes a range of choices from veryfast (best speed) to
# veryslow (best quality).
DEFAULT_PRESET = 'medium'
# keyframes minimum every 100 frames
DEFAULT_KEY_MIN = 100
# maximum amount of GOP size, maximum every 100 frames there will be a
# keyframe, together with -keyint_min this gives a keyframe every 100
# frames
DEFAULT_GOP = 100
# ffmpeg has scene detection. 0 (stands for false)
DEFAULT_SC_THRESHOLD = 0
