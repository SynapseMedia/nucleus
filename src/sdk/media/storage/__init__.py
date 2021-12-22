import requests

__author__ = "gmena"

# Session keep alive
session = requests.Session()

from . import remote  # noqa
from . import ingest  # noqa


__all__ = ["remote", "ingest", "session"]
