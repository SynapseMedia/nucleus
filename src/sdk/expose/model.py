from src.sdk.harvest.model import _Model
from src.sdk.harvest.fields import CIDString


class Codex(_Model):
    signature: str
    public_key: str
    media: CIDString
    metadata: CIDString
