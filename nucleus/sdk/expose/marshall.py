from __future__ import annotations

import hashlib
import dataclasses
import jwt


from dataclasses import dataclass
from nucleus.core.types import JSON, Raw, Any
from nucleus.sdk.storage import Store, Object

from .standard import SEP001
from .constants import SECRET_HASH_SIZE


@dataclass(slots=True)
class Broker:
    """Middleware class to handle storage and signature"""

    key: str
    store: Store

    def __post_init__(self):
        """Hashing for secret key"""
        blake2 = hashlib.blake2b(digest_size=SECRET_HASH_SIZE)
        blake2.update(self.key.encode("utf-8"))
        self.key = blake2.hexdigest()

    def sign(self, payload: Raw, **kwargs: Any):
        return jwt.encode(payload, self.key, **kwargs)

    def verify(self, sig: str, **kwargs: Any) -> bool:
        try:
            jwt.decode(sig, self.key, **kwargs)  # type: ignore
            return True
        except jwt.DecodeError as error:
            raise error


@dataclass
class StdDist:
    """SEP Standard Distribution"""

    broker: Broker

    def key(self) -> str:
        """Forwarding for internal broker key"""
        return self.broker.key

    def _store_payload(self, payload: Raw) -> Raw:
        """Store the payload claims values in IPFS and replace the full metadata with a CID.

        :param store: ipfs node client
        :return: raw copy of payload
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
            stored_object = self.broker.store(JSON(value))
            payload[key] = stored_object.hash
        return payload

    def sign(self, sep: SEP001) -> str:
        """Sign metadata with broker key.
        IMPORTANT! Storage-conversion happen adding raw meta into IPFS and replacing it with corresponding CID

        :param sep: standard implementation
        :return: jwt string
        :rtype: str
        """

        # get the algorithm from sep header
        alg = sep.header.alg
        # prepare header + payload to generate/sign the new jwt
        header = dataclasses.asdict(sep.header)
        payload = dataclasses.asdict(sep.payload)

        # first store the payload to then sign it
        payload = self._store_payload(payload)
        return self.broker.sign(payload, algorithm=alg, headers=header)

    def store(self, sig: str) -> Object:
        """Store metadata into IPFS

        :param sig: jwt signature
        :return: Object instance
        :rtype: Object
        """
        return self.broker.store(sig)

    def announce(self, sep: SEP001) -> Object:
        """Sign and store metadata into IPFS

        :param sep: standard implementation
        :return: Object with cid
        :rtype: Object
        """
        signature = self.sign(sep)
        return self.store(signature)

    def verify(self, sep: SEP001, sig: str) -> bool:
        """Verify standard signature:

        :param sep: the standard implementation
        :param sig: the jwt signature
        :return: True if valid signature for sep else False
        :rtype: bool
        """
        return self.broker.verify(sig, algorithms=[sep.header.alg])


__all__ = ("StdDist", "Broker")
