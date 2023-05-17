import pytest

# import responses
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
    KeyRing,
    DagJose,
    Sign,
    # Compact,
)


# @responses.activate
# @pytest.mark.skip(reason="need mocks")
def test_nucleus():
    """Should return valid Pin for valid CID"""

    LOCAL_ENDPOINT = "http://localhost:5001"
    FAKE_KEY = "ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY"

    # 1. prepare our model schema to collect/validate/clean data
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
        # TODO esta fallando
        image: Image = harvest.image(path=Path("example.jpg"))
        image_engine: Engine = processing.engine(image)
        image_engine.configure(Resize(720, 480))
        # finally save the processed image to our custom dir
        output_file: File = image_engine.save(Path("cat.jpg"))

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
        sep001 = expose.standard(media_type)  # image/jpeg
        sep001.add_metadata(Descriptive(**dict(nucleus)))
        sep001.add_metadata(Structural(cid=stored_file_object.hash))
        sep001.add_metadata(Technical(size=size, width=width, height=height))

        # init our standard distribution for sep001
        key = KeyRing()
        signed_jose = Sign(DagJose(sep001))
        signed_jose.add_key(key)
        # we get dag-jose signed.. let's store it
        serialized = signed_jose.serialize()
        obj: Object = serialized.save_to(local_storage)
        assert 0
        print(obj)

        # what we do with the CID?
