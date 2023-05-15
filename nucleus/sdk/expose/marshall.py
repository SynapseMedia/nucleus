from __future__ import annotations


import hashlib
import dataclasses
import functools
import json

import dag_cbor

from dataclasses import dataclass
from base64 import urlsafe_b64encode, b64encode
from nucleus.core.types import JSON, Raw, CID
from nucleus.sdk.storage import Object, Store

from .types import Serializer, SEP001
from .keyring import KeyRing


def cid_from_bytes(data: bytes, codec: str = "raw") -> CID:
    """Return a new CIDv1 base32 based on data hash and codec.

    :param data: the data to create a new CID
    :param codec: the codec to use for the new CID
    :return: the new multi format cid object
    :rtype: CID
    """
    digest = hashlib.sha256(data).digest()
    return CID.create("base32", 1, codec, ("sha2-256", digest))


def dispatch(sep: SEP001):

    # TODO singledispatch aca
    @functools.singledispatch
    # TODO el callable permite la firma por eso se devuelve un callback
    # eg marshall(local_storage)(dag_jose)(keyRing)
    def sign(serializer: Serializer) -> Callable[KeyRing, Any]:
        ...

    @serialize.register
    def _(serializer: DagJose):
        ...

    return serialize


@dataclass(slots=True)
class DagJose:
    """Dag-JOSE Serialization"""

    sep: SEP001

    def encode(self, kr: KeyRing) -> Raw:

        cbor_encoded = dag_cbor.encode(payload)
        cid = cid_from_bytes(cbor_encoded)
        cid_bytes = bytes(cid)
        header_bytes = bytes(JSON(header))

        payload_cid = urlsafe_b64encode(cid_bytes).rstrip(b"=").decode()
        header_encoded = urlsafe_b64encode(header_bytes).rstrip(b"=").decode()
        signing_input = ".".join([header_encoded, payload_cid])

        signature = kr.sign(signing_input)
        encoded_signature = urlsafe_b64encode(signature).rstrip(b"=").decode()

        # TODO new type
        return {
            "payload": f"{payload_cid}",
            "signatures": [
                {
                    "header": {"jwk": {}},  # TODO agrear aca jwk, alg, typ
                    "protected": f"{header_encoded}",
                    "signature": f"{encoded_signature}",
                }
            ],
            "link": f"{cid}",
        }


@dataclass(slots=True)
class Compact:
    """JWS Compact Serialization"""

    sep: SEP001

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

    def encode(self, kr: KeyRing) -> str:
        ...


__all__ = ("DagJose", "Compact")
