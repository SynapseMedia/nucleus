import requests

from urllib.parse import urljoin
from nucleus.core.types import Any


class LiveSession(requests.Session):
    """Enhance the session behavior by adding the default base url into requests"""

    _base_url: str

    def __init__(self, base_url: str):
        super().__init__()
        self._base_url = base_url

    def request(self, method: Any, url: Any, *args: Any, **kwargs: Any):
        """Same as Session request, we add an extra behavior to concat in every request the base url."""
        joined_url = urljoin(self._base_url, url)  # type: ignore
        return super().request(method, joined_url, *args, **kwargs)
