from __future__ import annotations


import hashlib
import dataclasses
import functools

import dag_cbor
from multiformats import CID as MFormatCID


from dataclasses import dataclass
from nucleus.core.types import JSON, Raw
from nucleus.sdk.storage import Object

from .types import Serializer, SEP001
from .keyring import KeyRing


def cid_from_bytes(data: bytes, codec: str = "raw") -> MFormatCID:
    """Return a new CIDv1 base32 based on data hash and codec.

    :param data: the data to create a new CID
    :param codec: the codec to use for the new CID
    :return: the new multi format cid object
    :rtype: MFormatCID
    """
    digest = hashlib.sha256(data).digest()
    return MFormatCID("base32", 1, codec, ("sha2-256", digest))


class DagJose(Serializer):
    """Dag-JOSE Serialization"""

    sep: SEP001


class Compact(Serializer):
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

    def payload(self) -> Raw:
        payload = dataclasses.asdict(self.sep.payload)
        return self._payload_cid_values(payload)


@dataclass
class Marshall:
    """Standard metadata distribution for SEP001 specification.
    This class is in charge of publishing metadata.
    """

    serializer: Serializer

    @functools.singledispatchmethod
    # TODO aca en base al serializar procesamos?
    def encode(self):
        ...

    def sign(self, ky: KeyRing) -> str:
        """Sign metadata with broker key.
        IMPORTANT! Storage-conversion happen adding raw meta into IPFS and replacing it with corresponding CID

        :param sep: standard implementation
        :return: jwt string
        :rtype: str
        """

        # get the algorithm from sep header
        alg = self.serializer.alg()
        # prepare header + payload to generate/sign the new jwt
        header = self.serializer.header()
        payload = self.serializer.payload()

        # first store the payload to then sign it
        return ky.sign(payload, algorithm=alg, headers=header)


__all__ = ("Marshall", "Compact")
