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
    Compact
    
)
from nucleus.sdk.harvest import Model, Video
from nucleus.sdk.processing import H264, HLS, Engine, File
from nucleus.sdk.storage import Object, Store


# @pytest.mark.skip(reason='no way of currently testing this. mock needed')
def test_main():
    LOCAL_ENDPOINT = 'http://localhost:5001'

    # 1. prepare our model schema to collect/validate/clean data
    with logger.console.status('Harvesting'):

        class Nucleus(Model):
            name: str
            description: str
            contributors: List[str]

        # set our data in the model
        nucleus: Model = Nucleus(
            name='Nucleus the SDK',
            description='Building block for multimedia decentralization',
            contributors=['Jacob', 'Geo', 'Dennis', 'Mark'],
        )

    # 2. init our processing engine based on our media model
    with logger.console.status('Processing'):
        # "infer" engine based on input media type
        video: Video = harvest.video(path=Path('sample.mp4'))
        video_engine: Engine = processing.engine(video)
        # transcode to HLS/H264
        video_engine.configure(HLS(H264()))

        # finally save the processed video
        output_file_name = 'index.m3u8'
        output_directory = Path('hls')

        if not output_directory.exists():
            output_directory.mkdir()

        # output HLS files to the new output path
        output_path = Path(f'{output_directory}/{output_file_name}')
        output_file: File = video_engine.save(output_path)

    # 3. store our processed image in local IPFS node and pin it in estuary
    with logger.console.status('Storage'):
        # since hls generate many different files in the same directory
        # we need to store the full directory. Dont worry we got your back ;).
        local_storage: Store = storage.ipfs(LOCAL_ENDPOINT)
        stored_file_object: Object = local_storage(output_directory)

    # 4. expose our media through the standard
    with logger.console.status('Expose'):
        # technical information about image
        length = float(output_file.meta.format.duration) * 1000
        size = int(output_file.meta.size)
        media_type = output_file.meta.type

        # standard implementation
        # https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
        sep001 = expose.standard(media_type)  # image/png
        # Prepare serialization
        sep001.set_operation(Sign)
        sep001.set_serialization(Compact)
        # Add signature/recipient key
        sep001.add_key(expose.es256())
        # add metadata into payload
        sep001.add_metadata(Descriptive(**dict(nucleus)))
        sep001.add_metadata(Technical(size=size, length=length))
        sep001.add_metadata(Structural(cid=stored_file_object.hash, path=output_file_name))
        # we get signed dag-jose serialization.. let's store it
        obj: Object = sep001.serialize().save_to(local_storage)
        # what we do with our new and cool CID?
        logger.console.print(obj.hash)

        assert 0

        """
        Lets try:
        
            ipfs dag get bagcqceraajwo66kumbcrxf2todw7wjrmayh7tjwaegwigcgpzk745my4qa5a
        
        """
