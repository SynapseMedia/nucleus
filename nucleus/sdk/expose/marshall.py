import dataclasses
import copy
import jwt

from dataclasses import dataclass, field
from nucleus.core.types import JSON, Union, Dict, Any
from nucleus.sdk.storage import Store
from .standard import SEP001


@dataclass
class StdDist:
    """Distributor handle SEP serialization and publish"""

    # we could add more SEPs eventually
    sep: SEP001
    _store: Union[Store, None] = field(init=False)
    _payload: Dict[Any, Any] = field(init=False)
    _header: Dict[Any, Any] = field(init=False)

    def __post_init__(self):
        self._store = None
        self._header = dataclasses.asdict(self.sep.header)
        # serialize payload omitting optional empty claims
        self._payload = dataclasses.asdict(
            self.sep.payload,
            dict_factory=lambda x: {k: v for k, v in x if v is not None},
        )

    def _store_payload(self) -> Dict[Any, Any]:
        """Store the payload claims values in IPFS and replace the full metadata with a CID.

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
        if not self._store:
            return self._payload

        sep_payload = copy.deepcopy(self._payload)
        for key, value in sep_payload.items():
            stored_object = self._store(JSON(value))
            sep_payload[key] = stored_object.hash
        return sep_payload

    def connect(self, store: Store):
        self._store = store

    def sign(self, secret: str) -> str:
        """Encode and sign jwt using the `standard` implementation

        :param secret: the secret to sign standard
        :return: jwt signature
        :rtype: str
        """
        return jwt.encode(
            self._store_payload(),
            secret,
            algorithm=self.sep.header.alg,
            headers=self._header,
        )
