import pytest
from src.core.exceptions import InvalidVideoQuality, InvalidStreamingProtocol
from src.core.media.transcode import REPR, Sizes, ProtocolID
from src.core.media.transcode.protocols import HLS, DASH
from src.core.media.transcode.factory import quality, streaming


def test_quality():
    """Should return a valid quality based on video size"""

    # Sizes hold each size as key and
    # each value as max quality supported
    sizes = {
        Sizes.Q480: REPR.R480p,
        Sizes.Q720: REPR.R720p,
        Sizes.Q1080: REPR.R1080p,
        Sizes.Q2k: REPR.R2k,
        Sizes.Q4k: REPR.R4k,
    }

    for size, high in sizes.items():
        representation = quality(size)
        # Expect always  the higher quality = size
        # expect always the lower quality = R360p
        higher = representation[-1]
        lower = representation[0]
        assert higher == high
        assert lower == REPR.R360p


def test_invalid_quality():
    """Should raise exception with invalid quality"""
    # All sized < 480 are not supported
    sizes = {
        Sizes.Q144,
        Sizes.Q240,
        Sizes.Q360,
    }

    for size in sizes:
        with pytest.raises(InvalidVideoQuality):
            quality(size)


def test_streaming_protocol():
    """Should return a valid streaming protocol for a valid protocol id"""

    with streaming(ProtocolID.HLS) as hls:
        assert isinstance(hls, HLS)
    with streaming(ProtocolID.DASH) as dash:
        assert isinstance(dash, DASH)


def test_invalid_streaming_protocol():
    """Should raise an exception for invalid protocol id"""

    with pytest.raises(InvalidStreamingProtocol):
        with streaming(0):
            pass