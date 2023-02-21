from src.sdk.harvest.model import Model
from src.sdk.harvest.fields import CIDString


class Codex(Model):
    signature: str
    publicKey: str
    media: CIDString
    metadata: CIDString
