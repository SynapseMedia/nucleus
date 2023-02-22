from __future__ import unicode_literals

from pydantic import types, networks
from pydantic.types import *  # type: ignore
from pydantic.networks import *  # type: ignore
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


__all__ = [*types.__all__, *networks.__all__, *["CIDString"]]  # type: ignore
