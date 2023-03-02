import requests
from src.core.types import Any


class GenericEdgeException(requests.exceptions.HTTPError):
    def __init__(self, message: str, *args: Any, **kwargs: Any):
        self.message = f"SDK :: Edge -> {message}"
        super(EdgePinException, self).__init__(*args, **kwargs)  # type: ignore


class EdgePinException(GenericEdgeException):
    ...
