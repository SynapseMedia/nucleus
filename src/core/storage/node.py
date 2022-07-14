from src.core.types import ID
from .types import CLI

def id() -> ID:
    """Return running ipfs node id"""
    exec = CLI("/id")
    output = exec().get("output")
    return output.get("ID")
