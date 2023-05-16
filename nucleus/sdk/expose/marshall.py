from __future__ import annotations


import hashlib
import dag_cbor

from jwcrypto.common import json_decode  # type: ignore
from nucleus.core.types import JSON, Raw, CID, Union, List, Any

from .signature import Sign, Serializer
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


class DagJose(Serializer):
    """Dag-JOSE Serialization"""

    _cbor: bytes
    _cid: CID

    def __init__(self, sep: SEP001):
        super().__init__(sep)
        # encode the payload as dag-cbor
        payload = vars(self._sep.payload)
        self._cbor = dag_cbor.encode(payload)
        self._cid = cid_from_bytes(self._cbor)
        self._assets = []

    def encode(self, jwt: Union[JWS, JWE]):
        """Encode JWS/JWE general serialization to dag-jose"""
        general_json = json_decode(jwt.serialize(False))  # type: ignore
        return {"link": self._cid, **general_json}

    def assets(self) -> List[Any]:
        """Assets could be used to return storable assets.
        eg. After generate CID from payload dag-cbor we need to store the bytes into blocks
        """
        return [self._cbor]

    def payload(self) -> bytes:
        """Serialize SEP using dag-jose IPLD standard
        ref: https://ipld.io/specs/codecs/dag-jose/spec/
        """
        return bytes(self._cid)


class Compact(Serializer):
    """JWS Compact Serialization"""

    def _payload_cid_values(self, payload: Raw) -> Raw:
        """Parse claims values to CIDs.

        :param payload: raw payload to parse
        :return: raw copy of processed payload
        :rtype: Raw

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
        return payload

    def payload(self) -> bytes:
        """SEP as compact serialization
        ref: https://www.rfc-editor.org/rfc/rfc7515#section-3.1
        """
        ...


__all__ = ("DagJose", "Compact", "Sign")
