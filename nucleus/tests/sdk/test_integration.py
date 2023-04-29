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
    Broker,
    StdDist,
)


# @responses.activate
@pytest.mark.skip(reason="need mocks")
def test_nucleus():
    """Should return valid Pin for valid CID"""

    LOCAL_ENDPOINT = "http://localhost:5001"
    FAKE_NODE_ID = "12D3KooWA86iJopk9FZcXdJZo8RpkFLV4D2qvKMsqCktiBzXTU11"
    FAKE_KEY = "ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY"

    # 1. prepare our model schema to collect/validate/clean data and publish it
    with logger.console.status("Harvesting"):

        class Nucleus(Model):
            name: str
            desc: str
            contributors: List[str]

        nucleus: Model = Nucleus.parse_obj(
            {
                "name": "Nucleus the SDK 1",
                "desc": "Building block for multimedia decentralization",
                "contributors": ["Jacob", "Geo", "Dennis", "Mark"],
            }
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
        edge_client: Edge = storage.service(estuary)
        edge_client.pin(stored_file_object)  # pin our cid in estuary

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

        # init our standard distribution for sep001
        broker: Broker = Broker(key=FAKE_NODE_ID, store=local_storage)
        distributor: StdDist = expose.dispatch(broker)
        stored_signature: Object = distributor.announce(sep001)

        # verify our standard signature
        key: str = distributor.key()
        signature: str = distributor.sign(sep001)

        assert distributor.verify(sep001, signature)
        assert key == "d673fef08feb368505b575a615183d8982133403ebbbe07fd8baa4b6d3ce52e2"
        assert (
            stored_signature.hash
            == "bafkreicxagdqix6okyzdcpnvuyahhewfd6vafujctxxdv6ckegrelzs5hm"
        )
