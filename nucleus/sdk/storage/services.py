from dataclasses import dataclass

from nucleus.core.types import URL


@dataclass(slots=True)
class Estuary:
    """Estuary API settings"""

    _endpoint: URL
    _key: str

    def endpoint(self) -> URL:
        return self._endpoint

    def key(self) -> str:
        return self._key


__all__ = ('Estuary',)
