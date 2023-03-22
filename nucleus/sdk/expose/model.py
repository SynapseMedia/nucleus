from nucleus.core.types import CID
from nucleus.sdk.harvest.model import _Model  # type: ignore


class Impulse(_Model):
    signature: str
    public_key: str
    media: CID
    metadata: CID
