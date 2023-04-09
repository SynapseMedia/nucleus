# import zlib

from dataclasses import asdict
from nucleus.core.types import CID, JSON
from nucleus.sdk.expose import SEP001, Header, Payload


def test_standard_size():
    """Should return all nested structs with a size less than 256 bytes"""
    header = Header(alg="HS256", typ="video/H264")
    payload = Payload(
        iat=1509654401,
        iss="0x71C7656EC7ab88b098defB751B7401B5f6d8976F",
        s=CID("QmVrrF7DTnbqKvWR7P7ihJKp4N5fKmBX29m5CHbW9WLep9"),
        d=CID("QmVrrF7DTnbqKvWR7P7ihJKp4N5fKmBX29m5CHbW9WLep9"),
    )

    std = SEP001(
        CID("bafkreiafogsmhi4yvuk7z4suhcr3rcnztqmt7rydgj3dmk6jeylmglnq5u"),  # 30 bytes
        CID("bafkreih53kxfrae2ectrgntv4ovcb5ox2mrqa63ymt5mr7sb6zrb34jcyy"),  # 182 bytes
    )

    header_as_bytes = bytes(JSON(asdict(header)))
    payload_as_bytes = bytes(JSON(asdict(payload)))
    as_bytes = bytes(JSON(asdict(std)))

    assert len(header_as_bytes) < 256
    assert len(payload_as_bytes) < 256
    assert len(as_bytes) < 256
