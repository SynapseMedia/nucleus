from nucleus.core.types import URL


class Estuary:
    """Estuary API settings.
    Implements Services
    """

    _endpoint: URL
    _key: str

    def endpoint(self) -> URL:
        return self._endpoint

    def key(self) -> str:
        return self._key
