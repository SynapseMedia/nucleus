import pydantic


class Codex(pydantic.BaseModel):
    signature: str
    publicKey: str
    hash: str
    media: str
    metadata: str
