import requests

__author__ = "gmena"

# Session keep alive
session = requests.Session()

from . import edge  # noqa
from . import local  # noqa


__all__ = ["edge", "local", "session"]
