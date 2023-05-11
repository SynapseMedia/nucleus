import pytest
import nucleus.core.logger as logger
import nucleus.sdk.harvest as harvest
import nucleus.sdk.processing as processing
import nucleus.sdk.storage as storage
import nucleus.sdk.expose as expose


from nucleus.core.types import List, Path
from nucleus.sdk.harvest import Image, Model
from nucleus.sdk.storage import Store, Service, Edge, Object
from nucleus.sdk.processing import Resize, Engine, File
from nucleus.sdk.expose import (
    Structural,
    Descriptive,
    Technical,
    Compact,
    Marshall,
)


# @responses.activate
# @pytest.mark.skip(reason="need mocks")
def test_nucleus():
    """Should return valid Pin for valid CID"""

    LOCAL_ENDPOINT = "http://localhost:5001"
    FAKE_KEY = "ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY"

    # 1. prepare our model schema to collect/validate/clean data and publish it
    with logger.console.status("Harvesting"):

        class Nucleus(Model):
            name: str
            desc: str
            contributors: List[str]

        # set our data in the model
        nucleus: Model = Nucleus(
            name="Nucleus the SDK",
            desc="Building block for multimedia decentralization",
            contributors=["Jacob", "Geo", "Dennis", "Mark"],
        )

    # 2. init our processing engine based on our media model
    with logger.console.status("Processing"):
        # "infer" engine based on input media type
        image: Image = harvest.image(path=Path("arch.png"))
        image_engine: Engine[Image] = processing.engine(image)
        image_engine.configure(Resize(50, 50))
        # finally save the processed image to our custom dir
        output_file: File = image_engine.save(Path("arch2.png"))

    # 3. store our processed image in local IPFS node and pin it in estuary
    with logger.console.status("Storage"):
        local_storage: Store = storage.ipfs(LOCAL_ENDPOINT)
        stored_file_object: Object = local_storage(output_file)

        # choose and connect an edge service to pin our resources. eg. estuary
        estuary: Service = storage.estuary(FAKE_KEY)  # estuary service
        # based on service get the client
        # edge_client: Edge = storage.service(estuary)
        # edge_client.pin(stored_file_object)  # pin our cid in estuary

    # 4. expose our media through the standard
    with logger.console.status("Expose"):
        # technical information about image
        size = output_file.meta.size
        width = output_file.meta.width
        height = output_file.meta.height
        media_type = output_file.meta.type

        # standard implementation
        # https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
        sep001 = expose.public(media_type)  # image/jpeg
        sep001.add_metadata(Descriptive(**dict(nucleus)))
        sep001.add_metadata(Structural(cid=stored_file_object.hash))
        sep001.add_metadata(Technical(size=size, width=width, height=height))

        import dag_cbor
        import hashlib
        import json
        from multiformats import CID
        from base64 import urlsafe_b64encode, b64encode
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives import hashes
        from nucleus.core.types import JSON

        header = json.dumps({"alg": "ES256K", "typ": "image/png"})
        payload = {
            "s": {"cid": "bafkzvzacdkfkzvcl4xqmnelaobsppwxahpnqvxhui4rmyxlaqhrq"},
            "d": {
                "name": "Nucleus the SDK 1",
                "desc": "Building block for multimedia decentralization",
                "contributors": ["Jacob", "Geo", "Dennis", "Mark"],
            },
            "t": {"size": 3495, "width": 50, "height": 50},
            "r": {},
        }

        # este proceso es equivalente a agregar el payload en dag y luego usar el cid bytes
        cbor = dag_cbor.encode(payload)
        hashed = hashlib.sha256(bytes(JSON(payload["s"])))
        digest = hashed.digest()

        cid = CID("base32", 1, "raw", ("sha2-256", digest))
        assert 0
        cid_bytes = bytes(cid)

        payload_cid = urlsafe_b64encode(cid_bytes).rstrip(b"=").decode()
        header_encoded = urlsafe_b64encode(header.encode()).rstrip(b"=").decode()
        signing_input = ".".join([header_encoded, payload_cid])
        signature = distributor.key().private.sign(
            signing_input.encode(), ec.ECDSA(hashes.SHA256())
        )

        encoded_signature = urlsafe_b64encode(signature).rstrip(b"=").decode()
        jwt = ".".join([header_encoded, payload_cid, encoded_signature])
        store_cid = local_storage(cbor)

        result = {
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

        # init our standard distribution for sep001
        serialization: Compact = Compact(sep001)
        distributor: Marshall = expose.dispatch(serialization)
        stored_signature: Object = distributor.announce(sep001)

        # # verify our standard signature
        # signature: str = distributor.sign(sep001)
        # assert distributor.verify(sep001, signature)
