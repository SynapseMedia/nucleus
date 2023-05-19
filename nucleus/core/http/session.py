from urllib.parse import urljoin

import requests

from nucleus.core.exceptions import HttpError
from nucleus.core.types import Any


class LiveSession(requests.Session):
    """Enhance the session behavior by adding the default base url into requests"""

    _base_url: str

    def __init__(self, base_url: str):
        super().__init__()
        self._base_url = base_url

    def request(self, method: Any, url: Any, *args: Any, **kwargs: Any):
        """Same as Session request, we add an extra behavior to concat in every request the base url."""

        # auto concatenate base url with request path
        joined_url = urljoin(self._base_url, url)  # type: ignore

        try:
            return super().request(method, joined_url, *args, **kwargs)
        except requests.exceptions.RequestException as e:
            raise HttpError(f'error trying to make a request to {joined_url}: {str(e)}')
