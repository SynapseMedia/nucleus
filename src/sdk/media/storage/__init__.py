import requests

__author__ = "gmena"

# Session keep alive
session = requests.Session()

from . import edge  # noqa
from . import ingest  # noqa


__all__ = ["edge", "ingest", "session"]
