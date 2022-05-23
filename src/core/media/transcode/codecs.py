from . import Codec
from ffmpeg_streaming import Representation

#TODO builder pattern
class HLS(Codec):
    def __init__(self, input: Input):
        super().__init__()
        self._hls = input.hls()
        
    def set_representation(self, repr: Representation):
        self.input.dash(repr)
        pass
    
    def set_quality():
        pass
    
    def format():
        return Formats.h264()
    
    def transcode():
        pass