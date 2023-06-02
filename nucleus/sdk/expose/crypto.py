from __future__ import annotations

from dataclasses import dataclass, field

from jwcrypto.common import json_encode  # type: ignore

from .types import JWS, KeyRing, Serializer


@dataclass(slots=True)
class Sign:

    """Sign is in charge of JWS serialization"""

    # attach serializer as subscriber
    _s8r: Serializer
    # internal JWS interface
    _jws: JWS = field(init=False)

    def __post_init__(self):
        """Initialize JWS instance
        ref: https://jwcrypto.readthedocs.io/en/latest/jws.html
        """
        self._jws = JWS(bytes(self._s8r))

    def add_key(self, kr: KeyRing) -> Sign:
        """Bind signers to JWS

        :param kr: keyring to assoc with signature
        :return: JWS object
        :rtype: JWS
        """

        header = {**dict(kr), **dict(self._s8r)}
        self._jws.add_signature(kr.jwk, None, json_encode(header))  # type: ignore
        return self

    def serialize(self) -> Serializer:
        """Trigger and notify to underneath serializer for JWS post-processing .
        In this step additional data could be added/modified into JWS.

        :return: an out of the box serializer
        :rtype: Serializer
        """
        return self._s8r.update(self._jws)


class Cypher(Sign):
    # TODO pending implementation
    ...


__all__ = ('Sign', 'Cypher')
