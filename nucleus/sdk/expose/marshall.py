from __future__ import annotations

import hashlib

import dag_cbor
from jwcrypto.common import json_decode  # type: ignore

from nucleus.core.types import CID, JSON, List, Raw, Union
from nucleus.sdk.storage import Object, Store

from .types import JWE, JWS, Standard


def cid_from_bytes(data: bytes, codec: str = 'raw') -> CID:
    """Return a new CIDv1 base32 based on data hash and codec.

    :param data: the data to create a new CID
    :param codec: the codec to use for the new CID
    :return: the new multi format cid object
    :rtype: CID
    """
    digest = hashlib.sha256(data).digest()
    return CID.create('base32', 1, codec, ('sha2-256', digest))


class DagJose:
    """Dag-JOSE Serialization observer"""

    _cid: CID
    _s11n: JSON
    _cbor: bytes
    _header: Raw
    _std: Standard

    def __init__(self, standard: Standard):
        self._header = standard.header()
        self._cbor = dag_cbor.encode(standard.payload())
        self._cid = cid_from_bytes(self._cbor, 'dag-cbor')

    def __iter__(self):
        return iter(self._header.items())

    def __str__(self):
        return str(self._s11n)

    def __bytes__(self) -> bytes:
        """Serialize SEP using dag-jose IPLD standard
        ref: https://ipld.io/specs/codecs/dag-jose/spec/
        """
        return bytes(self._cid)

    def update(self, jwt: Union[JWS, JWE]) -> DagJose:
        """Encode JWS/JWE general serialization to dag-jose when crypto process get ready"""
        general_json = json_decode(jwt.serialize(False))  # type: ignore
        # set new state for serialization attribute
        self._s11n = JSON({'link': self._cid, **general_json})
        return self

    def save_to(self, store: Store) -> Object:
        # 1. store cbor in blocks
        # 2. store serialization and return
        store(self._cbor)
        return store(self._s11n)


class Compact:
    """JWS Compact Serialization"""

    _s11n: str
    _header: Raw
    _payload: JSON
    _claims: List[bytes] = []

    def __init__(self, standard: Standard):
        self._header = standard.header()
        raw_payload = standard.payload()
        self._claims = list(map(bytes, map(JSON, raw_payload.values())))
        self._payload = self._payload_cid_values(raw_payload)

    def _payload_cid_values(self, payload: Raw) -> JSON:
        """Parse claims values to CIDs.

        :param payload: payload to parse
        :return: copy of processed payload
        :rtype: JSON

        eg.
            {
                's': {'cid': 'bafkzvzacdkfkzvcl4xqmnelaobsppwxahpnqvxhui4rmyxlaqhrq'},
                'd': {
                    'name': 'Nucleus the SDK 1',
                    'desc': 'Building block for multimedia decentralization',
                    'contributors': ['Jacob', 'Geo', 'Dennis', 'Mark']
                },
                't': {'size': 3495, 'width': 50, 'height': 50}}
            =>
            {
                's': 'bafkzvzacdiiynlkns53exjiv2ix7p7a4slc2aifwh5ijzqywbtgq',
                'd': 'bafkzvzacdldmi4t4s5qhhvgguuzzamgv2kqijhjak4ihwojezukq',
                't': 'bafkzvzacdkg4xam57fkxjno3uogkkchuqhclf32kmgnuwsl4ugaa'
            }
        """

        for key, value in payload.items():
            raw_claim = bytes(JSON(value))
            payload[key] = str(cid_from_bytes(raw_claim))
        return JSON(payload)

    def update(self, jwt: Union[JWS, JWE]) -> Compact:
        """Encode JWS/JWE compact serialization when  crypto process get ready"""
        # set new state for serialization attribute
        self._s11n = jwt.serialize(True)  # type: ignore
        return self

    def save_to(self, store: Store) -> Object:
        # 1. store claims in blocks
        for claim in self._claims:
            store(claim)

        # 2. store serialization and return
        return store(self._s11n)

    def __iter__(self):
        return iter(self._header.items())

    def __str__(self):
        return self._s11n

    def __bytes__(self) -> bytes:
        """SEP as compact serialization
        ref: https://www.rfc-editor.org/rfc/rfc7515#section-3.1
        """
        return bytes(self._payload)


__all__ = ('DagJose', 'Compact')
