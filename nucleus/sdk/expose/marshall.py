from __future__ import annotations


import hashlib
import dag_cbor

from abc import ABC, abstractmethod
from jwcrypto.common import json_decode  # type: ignore
from nucleus.core.types import JSON, Raw, CID, Union, List
from nucleus.sdk.storage import Store, Object

from .standard import SEP001
from .types import JWS, JWE


def cid_from_bytes(data: bytes, codec: str = "raw") -> CID:
    """Return a new CIDv1 base32 based on data hash and codec.

    :param data: the data to create a new CID
    :param codec: the codec to use for the new CID
    :return: the new multi format cid object
    :rtype: CID
    """
    digest = hashlib.sha256(data).digest()
    return CID.create("base32", 1, codec, ("sha2-256", digest))


class Serializer(ABC):
    """Serializer observer/template specifies the methods needed to handle SEP001 serialization.
    Defines how to handle serialization for each strategy according to the specification, which includes:

    - Compact
    - DAG-JOSE

    This template class must be implemented by other classes that provide concrete serialization logic.
    ref: https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    _sep: SEP001

    def __init__(self, sep: SEP001):
        self._sep = sep

    def header(self) -> Raw:
        """Return the type of data to process"""
        return vars(self._sep.header)

    @abstractmethod
    def save_to(self, store: Store) -> Object:
        """Could be used to store assets.
        eg. After generate CID from payload dag-cbor we need to store the bytes into blocks
        """

        ...

    @abstractmethod
    def update(self, jwt: Union[JWS, JWE]) -> Serializer:
        """Receive updates when serialization is ready to handle any additional encoding step.
        In this step we could add a new state or operate over JWS/JWE to handle any additional encoding.

        :param jwt: JWT to handle
        :return: ready to use Serializer
        :rtype: Serializer
        """
        ...

    @abstractmethod
    def __str__(self) -> str:
        """The serialized data as string"""
        ...

    @abstractmethod
    def __bytes__(self) -> bytes:
        """The payload data ready to sign/encrypt"""
        ...


class DagJose(Serializer):
    """Dag-JOSE Serialization observer"""

    _cbor: bytes
    _cid: CID
    _s11n: JSON

    def __init__(self, sep: SEP001):
        super().__init__(sep)
        # encode the payload as dag-cbor
        payload = vars(sep.payload)
        self._cbor = dag_cbor.encode(payload)
        self._cid = cid_from_bytes(self._cbor, "dag-cbor")

    def update(self, jwt: Union[JWS, JWE]) -> DagJose:
        """Encode JWS/JWE general serialization to dag-jose when crypto process get ready"""
        general_json = json_decode(jwt.serialize(False))  # type: ignore
        # set new state for serialization attribute
        self._s11n = JSON({"link": self._cid, **general_json})
        return self

    def save_to(self, store: Store) -> Object:
        # 1. store cbor in blocks
        # 2. store serialization and return
        store(self._cbor)
        return store(self._s11n)

    def __str__(self):
        return str(self._s11n)

    def __bytes__(self) -> bytes:
        """Serialize SEP using dag-jose IPLD standard
        ref: https://ipld.io/specs/codecs/dag-jose/spec/
        """
        return bytes(self._cid)


class Compact(Serializer):
    """JWS Compact Serialization"""

    _s11n: str
    _payload: JSON
    _claims: List[bytes] = []

    def __init__(self, sep: SEP001):
        super().__init__(sep)

        # prepare payload and claims
        raw_payload = vars(self._sep.payload)
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
        # 1. store cbor in blocks
        # 2. store serialization and return
        map(store, self._claims)
        return store(self._s11n)

    def __str__(self):
        return self._s11n

    def __bytes__(self) -> bytes:
        """SEP as compact serialization
        ref: https://www.rfc-editor.org/rfc/rfc7515#section-3.1
        """
        return bytes(self._payload)


__all__ = ("DagJose", "Compact")
