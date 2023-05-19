import nucleus.sdk.expose as expose
from nucleus.core.types import CID
from nucleus.sdk.expose import Descriptive, Structural, Technical


def test_standard():
    """Should return standard struct with valid header and payload"""

    standard = expose.standard('video/H264')
    # expected data
    size = 10
    desc = 'Test'
    title = 'Hello world'
    cid = CID('bafkreiafogsmhi4yvuk7z4suhcr3rcnztqmt7rydgj3dmk6jeylmglnq5u')

    standard.add_metadata(Structural(cid=cid))
    standard.add_metadata(Descriptive(title=title, desc=desc))
    standard.add_metadata(Technical(size=size))

    header = standard.header()
    payload = standard.payload()

    assert header == {'typ': 'video/H264'}
    assert payload == {
        's': {'cid': cid},
        'd': {'title': title, 'desc': desc},
        't': {'size': size},
    }
