from src.sdk.media.transcode.codecs import get_representations, REPR


# Unit tests
def test_valid_representation_returned_with_valid_resolution():
    """Should return a valid representation based on resolution"""
    quality_to_test = (
        ("360p", [REPR.R360p]),
        ("480p", [REPR.R360p, REPR.R480p]),
        ("720p", [REPR.R360p, REPR.R480p, REPR.R720p]),
        ("1080p", [REPR.R360p, REPR.R480p, REPR.R720p, REPR.R1080p]),
        ("2k", [REPR.R360p, REPR.R480p, REPR.R720p, REPR.R1080p, REPR.R2k]),
        ("4k", [REPR.R360p, REPR.R480p, REPR.R720p, REPR.R1080p, REPR.R2k, REPR.R4k]),
    )

    for q, r in quality_to_test:
        assert get_representations(q) == r
