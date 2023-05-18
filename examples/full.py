import nucleus.core.logger as logger
import nucleus.sdk.harvest as harvest
import nucleus.sdk.processing as processing
import nucleus.sdk.storage as storage
import nucleus.sdk.expose as expose

from nucleus.core.types import List, Path
from nucleus.sdk.harvest import Image, Model
from nucleus.sdk.storage import Store, Service, Client, Object
from nucleus.sdk.processing import Resize, Engine, File
from nucleus.sdk.expose import (
    Structural,
    Descriptive,
    Technical,
    DagJose,
    # Compact
)


def main():

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
        image: Image = harvest.image(path=Path("arch.png"))
        image_engine: Engine = processing.engine(image)
        image_engine.configure(Resize(50, 50))
        # finally save the processed image to our custom dir
        output_file: File = image_engine.save(Path("arch2.png"))

    # 3. store our processed image in local IPFS node and pin it in estuary
    with logger.console.status("Storage"):
        local_storage: Store = storage.ipfs(LOCAL_ENDPOINT)
        stored_file_object: Object = local_storage(output_file)
        # choose and connect an edge service to pin our resources. eg. estuary
        estuary: Service = storage.estuary(FAKE_KEY)
        edge_client: Client = storage.client(estuary)
        edge_client.pin(stored_file_object)

    # 4. expose our media through the standard
    with logger.console.status("Expose"):
        # technical information about image
        size = output_file.meta.size
        width = output_file.meta.width
        height = output_file.meta.height
        media_type = output_file.meta.type

        # standard implementation
        # https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
        sep001 = expose.standard(media_type)  # image/png
        sep001.set_method(DagJose)  # set serialization method
        sep001.add_metadata(Descriptive(**dict(nucleus)))
        sep001.add_metadata(Structural(cid=stored_file_object.hash))
        sep001.add_metadata(Technical(size=size, width=width, height=height))
        # define signature type for method eg. ES256 algorithm
        signed_dag_jose = sep001.sign(expose.es256())
        # we get signed dag-jose serialization.. let's store it
        obj: Object = signed_dag_jose.save_to(local_storage)
        # what we do with our new and cool CID?
        logger.console.print(obj.hash)

        """
        Lets try:
        
            ipfs dag get bagcqceraajwo66kumbcrxf2todw7wjrmayh7tjwaegwigcgpzk745my4qa5a
        
        Output:
        
            {
                "link": {
                    "/": "bafyreicjeouqwpslvdjm7nznimlvhdiibv6icucr73eqw56sm23kbs3yfy"
                },
                "payload": "AXESIEkjqQs-S6jSz7ctQxdTjQgNfIFQUf7JC3fSZragy3gu",
                "signatures": [
                    {
                    "protected": "eyJhbGciOiJFUzI1NksiLCJqd2siOnsiYWxnIjoiRVMyNTZLIiwiY3J2Ijoic2VjcDI1NmsxIiwiZCI6IlFzVEtGY2pfSVE5VnQxWjc2S0F5V3V2ZzdROHNTRm4taXA1MWxyQm9hc3MiLCJrdHkiOiJFQyIsInVzZSI6InNpZyIsIngiOiJqLTlzOEZVTExCdmFnRm9yeE9FcmVGbUVKOUd4R19EU3dmaG1EYXNtY0hvIiwieSI6Imktc0R6cU5tRXZIVTFPcll3MHRfN2wtZG5razFEQ0pqNTRiaUthX1FsdVEifSwidHlwIjoiaW1hZ2UvcG5nIn0",
                    "signature": "CK1djEEuVuyBlr2uA9RvJL86sgpgZnyf2jL59_imQ4xU5-88CNQ-kHbORkUigde43bNPzO-ylxM0eIm9GgXpqw"
                    }
                ]
            }
        
        """
