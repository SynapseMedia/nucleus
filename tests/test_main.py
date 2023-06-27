import pytest

import nucleus.core.logger as logger
import nucleus.sdk.expose as expose
import nucleus.sdk.harvest as harvest
import nucleus.sdk.processing as processing
import nucleus.sdk.storage as storage
from nucleus.core.types import List, Path
from nucleus.sdk.expose import (
    DagJose,
    Descriptive,
    Sign,
    Structural,
    Technical,
)
from nucleus.sdk.harvest import Video, Model
from nucleus.sdk.processing import Engine, File, HLS, H264
from nucleus.sdk.storage import Object, Store, Client


@pytest.mark.skip(reason='no way of currently testing this. mock needed')
def test_main():
    LOCAL_ENDPOINT = "http://localhost:5001"
    FAKE_KEY = "EST2bf02f6d-c48d-4868-90c9-7015ab6d0b74ARY"

    # 1. prepare our model schema to collect/validate/clean data
    with logger.console.status("Harvesting"):

        class Nucleus(Model):
            name: str
            description: str
            contributors: List[str]

        # set our data in the model
        nucleus: Model = Nucleus(
            name="Nucleus the SDK",
            description="Building block for multimedia decentralization",
            contributors=["Jacob", "Geo", "Dennis", "Mark"],
        )

    # 2. init our processing engine based on our media model
    with logger.console.status("Processing"):
        # "infer" engine based on input media type
        video: Video = harvest.video(path=Path("sample.mp4"))
        image_engine: Engine = processing.engine(video)
        # transcode to HLS/H264
        image_engine.configure(HLS(H264()))
        # finally save the processed image to our custom dir
        output_file: File = image_engine.save(Path("sample.m3u8"))

    # 3. store our processed image in local IPFS node and pin it in estuary
    with logger.console.status("Storage"):
        local_storage: Store = storage.ipfs(LOCAL_ENDPOINT)
        stored_file_object: Object = local_storage(output_file)
        # choose and connect an edge service to pin our resources. eg. estuary
        # estuary: Client = storage.estuary(FAKE_KEY)
        # estuary.pin(stored_file_object)

    # 4. expose our media through the standard
    with logger.console.status("Expose"):
        # technical information about image
        length = float(output_file.meta.format.duration) * 1000
        size = int(output_file.meta.size)
        media_type = output_file.meta.type

        # standard implementation
        # https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
        sep001 = expose.standard(media_type)  # image/png
        # Prepare serialization
        sep001.set_operation(Sign)
        sep001.set_serialization(DagJose)
        # Add signature/recipient key
        sep001.add_key(expose.es256())
        # add metadata into payload
        sep001.add_metadata(Descriptive(**dict(nucleus)))
        sep001.add_metadata(Structural(cid=stored_file_object.hash))
        sep001.add_metadata(Technical(size=size, length=length))
        # we get signed dag-jose serialization.. let's store it
        obj: Object = sep001.serialize().save_to(local_storage)
        # what we do with our new and cool CID?
        logger.console.print(obj.hash)

        assert 0

        """
        Lets try:
        
            ipfs dag get bagcqceraajwo66kumbcrxf2todw7wjrmayh7tjwaegwigcgpzk745my4qa5a
        
        """
