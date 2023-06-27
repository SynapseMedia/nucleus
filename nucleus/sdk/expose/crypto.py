from __future__ import annotations

from dataclasses import dataclass, field

from jwcrypto.common import json_encode

from .types import JWS, Keyring, Serializer


@dataclass(slots=True)
class Sign:
    """JWS serialization implementation."""

    # attach serializer as subscriber
    _s8r: Serializer
    # internal JWS interface
    _jws: JWS = field(init=False)

    def __post_init__(self):
        # Initialize JWS instance
        self._jws = JWS(bytes(self._s8r))

    def add_key(self, kr: Keyring) -> Sign:
        """Bind signature keys to JWS serialization.

        :param kr: Keyring to assoc with signature
        :return: Sign object
        """

        header = {**dict(kr), **dict(self._s8r)}
        self._jws.add_signature(kr.jwk(), None, json_encode(header))
        return self

    def serialize(self) -> Serializer:
        """Trigger and notify to underneath serializer for JWS post-processing .
        In this step additional data could be added/modified into JWS.

        :return: The ready to use serializer object
        """
        return self._s8r.update(self._jws)


class Cypher(Sign):
    # TODO pending implementation
    ...


__all__ = ('Sign', 'Cypher')
