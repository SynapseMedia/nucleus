import responses
import nucleus.sdk.harvest as harvest
import nucleus.sdk.processing as processing
import nucleus.sdk.storage as storage

from nucleus.core.types import List, Path
from nucleus.sdk.harvest import Image, Meta
from nucleus.sdk.processing import Resize, Engine, File
from nucleus.sdk.storage import Pin, Store, Service, Edge, Object


@responses.activate
def test_nucleus():
    """Should return valid Pin for valid CID"""

    LOCAL_ENDPOINT = "http://localhost:5001"
    FAKE_KEY = "ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY"

    """ 
    1. lets define our model schema
    alternative:
    
        nucleus_model = harvest.meta(
            name=(str, ...),
            desc=(str, ...),
            contributors=(List[str], ...),
        )
    
    """

    class Nucleus(Meta):
        name: str
        desc: str
        contributors: List[str]

    # 2. collect new data to process and use the model to standardize it
    nucleus: Meta = Nucleus.parse_obj(
        {
            "name": "Nucleus the SDK",
            "desc": "Building block for multimedia decentralization",
            "contributors": ["Jacob", "Geo", "Dennis", "Mark"],
        }
    )

    # 3. prepare our media model
    image: Image = harvest.image(route=Path("arch.png"))

    # 4. init our engine based on our media model
    # "infer" engine based on input media type
    image_engine: Engine[Image] = processing.engine(image)
    image_engine.configure(Resize(50, 50))
    # finally save the processed image to our custom dir
    output_file: File = image_engine.save(Path("arch2.png"))

    # 5. store our processed image in local IPFS node
    local_node: Store = storage.ipfs(LOCAL_ENDPOINT)
    stored_file: Object = local_node(output_file)

    # 6. choose and connect an edge service to pin our resources. eg. estuary
    estuary: Service = storage.estuary(FAKE_KEY)  #  estuary service
    edge_client: Edge = storage.service(estuary)  #  based on service get the client
    pin: Pin = edge_client.pin(stored_file.hash)

    # 7. expose our media through the standard

    meta_expose = ...
