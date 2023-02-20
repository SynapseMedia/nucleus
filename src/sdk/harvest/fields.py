from src.core.types import CID


class CIDString(str):
    """Add to pydantic a new field support for CID strings"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        if not CID(v).valid():
            raise ValueError("string must be a CID")
