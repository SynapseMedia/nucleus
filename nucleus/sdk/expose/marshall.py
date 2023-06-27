from __future__ import annotations

import hashlib

import dag_cbor
from jwcrypto.common import json_decode

from nucleus.core.types import CID, JSON, List, Raw, Setting
from nucleus.sdk.storage import Object, Store

from .types import JWT, Standard


def _cid_from_bytes(data: bytes, codec: str = 'raw') -> CID:
    """Return a new CIDv1 base32 based on data hash and codec.

    :param data: The data to create a new CID
    :param codec: The codec to use for the new CID
    :return: The new multi format cid object
    """
    digest = hashlib.sha256(data).digest()
    return CID.create('base32', 1, codec, ('sha2-256', digest))


class DagJose:
    """Dag-JOSE serializer implementation."""

    _cid: CID
    _s11n: JSON
    _cbor: bytes
    _header: Raw
    _std: Standard

    def __init__(self, standard: Standard):
        """Initialize a new instance with the standard implementation.

        :param standard: Standard object
        """
        self._header = standard.header()
        self._cbor = dag_cbor.encode(standard.payload())
        self._cid = _cid_from_bytes(self._cbor, 'dag-cbor')

    def __iter__(self) -> Setting:
        """Yield `typ` headers specified in SEP-001 standard.

        :return: The iterable media type settings
        """
        return iter(self._header.items())

    def __str__(self) -> str:
        """Return DAG-JOSE serialization as string.

        :return:
        """
        return str(self._s11n)

    def __bytes__(self) -> bytes:
        """Return DAG-JOSE serialization as bytes.

        :return:
        """
        return bytes(self._cid)

    def update(self, jwt: JWT) -> DagJose:
        """Acts as an observer, waiting for events triggered by any cryptographic operation.
        Encodes JWS/JWE to DAG-JOSE serialization when a cryptographic operation notifies.

        :param jwt: The JWT implementation passed by the cryptographic operation.
        :return: The DAG-JOSE serialization format.
        """
        general_json = json_decode(jwt.serialize(False))
        # set new state for serialization attribute
        self._s11n = JSON({'link': self._cid, **general_json})
        return self

    def save_to(self, store: Store) -> Object:
        """Publishes DAG-JOSE into the local store.

        :param store: The Store function
        :return:
        """

        # 1. store cbor in blocks
        # 2. store serialization and return
        store(self._cbor)
        return store(self._s11n)


class Compact:
    """JWS Compact serializer implementation."""

    _s11n: str
    _header: Raw
    _payload: JSON
    _claims: List[bytes] = []

    def __init__(self, standard: Standard):
        """Initialize a new instance with the standard implementation.

        :param standard: Standard object
        """

        raw_payload = standard.payload()
        self._header = standard.header()
        self._claims = list(map(bytes, map(JSON, raw_payload.values())))
        self._payload = self._payload_cid_values(raw_payload)

    def _payload_cid_values(self, payload: Raw) -> JSON:
        """Parse claims values to CIDs.

        :param payload: Payload to parse
        :return: Copy of processed payload

        eg.
            {
                's': {'cid': 'bafkzvzacdkfkzvcl4xqmnelaobsppwxahpnqvxhui4rmyxlaqhrq'},
                'd': {
                    'name': 'Nucleus the SDK 1',
                    'description': 'Building block for multimedia decentralization',
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
            payload[key] = str(_cid_from_bytes(raw_claim))
        return JSON(payload)

    def update(self, jwt: JWT) -> Compact:
        """Acts as an observer, waiting for events triggered by any cryptographic operation.
        Encodes JWS/JWE to compact serialization when a cryptographic operation notifies.

        :param jwt: The JWT implementation passed by the cryptographic operation.
        :return: The compact serialization string.
        """
        # set new state for serialization attribute
        self._s11n = jwt.serialize(True)
        return self

    def save_to(self, store: Store) -> Object:
        """Publishes Compact serialization into the local store.

        :param store: The Store function
        :return:
        """

        # 1. store claims in blocks
        for claim in self._claims:
            store(claim)

        # 2. store serialization and return
        return store(self._s11n)

    def __iter__(self) -> Setting:
        """Yield `typ` headers specified in SEP-001 standard.

        :return: The iterable media type settings
        """
        return iter(self._header.items())

    def __str__(self) -> str:
        """Return compact serialization as string.

        :return:
        """
        return self._s11n

    def __bytes__(self) -> bytes:
        """Return compact serialization as bytes.

        :return:
        """
        return bytes(self._payload)


__all__ = ('DagJose', 'Compact')
