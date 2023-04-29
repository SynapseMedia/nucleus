# Nucleus

[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
[![Gitter](https://badges.gitter.im/watchit-app/community.svg)](https://gitter.im/watchit-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![CI](https://github.com/ZorrillosDev/watchit-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ZorrillosDev/watchit-toolkit/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ZorrillosDev/watchit-toolkit/branch/v0.4.0/graph/badge.svg?token=M9FF5B6UNA)](https://codecov.io/gh/ZorrillosDev/watchit-toolkit)

<img src="arch.png"
    alt="Markdown Monster icon"
    style="margin: 10px auto" />

***NOTE!*** Nucleus is **alpha-stage** software. It means nucleus hasn't been security audited and programming APIs and data formats can still change.

Nucleus its a low level compilation of "toolchain" for media decentralization.
It includes:

- Metadata harvesting
- Multimedia processing
- Multimedia storage
- Metadata distribution
- Web3 instruments

The design so far contains 3 layers of abstraction:

1. **The Core**: "The building block" packages here are intended to have minimal or no dependencies, those that have dependencies will be with the same internal packages and as far as possible they will be utility packages.

2. **The SDK**: Exposes the API to the client at the programming level to use core functions in a safe and conformant way.

3. **The CLI and HTTP API**: These make use of the sdk to form the services.

## Summary

Nucleus proposes a sequence of steps (pipeline) for the processing and decentralization of multimedia.

1. **Harvesting**: metadata collection
2. **Processing**: media processing
3. **Storage**:  storage in IPFS network
4. **Expose**: metadata imprinted onto the DHT
5. **Mint**: mint meta as NFTs
6. **Retrieval**: unmarshall and distribution of metadata

The pipeline design was based on the decoupling principle, allowing for different use cases. For instance, some elements such as the **storage** component may be optional if data is already stored on the IPFS network, or the **mint** component may be optional if there is no need to create NFTs for the metadata. Similarly, the **processing** component may not be necessary if the media is ready for storage.

"Retrieval" is an auxiliary component that allows for the retrieval and unmarshalling of data from the DHT as raw information that can then be used for distribution through any available or preferred means. In our case, we use Orbit as a distributed ledger for the "out of the box" consumption of our metadata.

## Full Example

```python
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


def main():

    LOCAL_ENDPOINT = "http://localhost:5001"
    FAKE_NODE_ID = "12D3KooWA86iJopk9FZcXdJZo8RpkFLV4D2qvKMsqCktiBzXTU11"
    FAKE_ESTUARY_KEY = "ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY"

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
        estuary: Service = storage.estuary(FAKE_KEY)  #  estuary service
        edge_client: Edge = storage.service(estuary)  #  based on service get the client
        edge_client.pin(stored_file_object)  # pin our cid in estuary

    # 4. expose our media through the standard
    with logger.console.status("Expose"):
        # technical information about image
        size = output_file.meta.size
        width = output_file.meta.width
        height = output_file.meta.height
        media_type = output_file.meta.type

        # standard implementation https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
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

    # assert expected behaviors
    assert distributor.verify(sep001, signature) == True
    assert key == "d673fef08feb368505b575a615183d8982133403ebbbe07fd8baa4b6d3ce52e2"
    assert stored_signature.hash  == "bafkreicxagdqix6okyzdcpnvuyahhewfd6vafujctxxdv6ckegrelzs5hm"
    assert stored_signature.name == 'bafkreicxagdqix6okyzdcpnvuyahhewfd6vafujctxxdv6ckegrelzs5hm'
    assert stored_signature.size == 443


```

## Installing

Before using `nucleus`, FFmpeg and IPFS must be installed.

1) Check the official docs to [install IPFS](https://docs.ipfs.tech/install/command-line/#system-requirements).
2) There are a variety of ways to install FFmpeg, such as the [official download links](https://ffmpeg.org/download.html), or using your package manager of choice (e.g. `sudo apt install ffmpeg` on Debian/Ubuntu, `brew install ffmpeg` on OS X, etc.).

## Development

Some available capabilities for dev support:

- **Install**: `make bootstrap`
- **Tests**: `make test`
- **Debug**: `make test-debug`
- **Lint**: `make code-check`
- **Lint Fix**: `make code-fix`

Note: Please check [Makefile](https://github.com/SynapseMedia/nucleus/blob/main/Makefile) for more capabilities.  

<!-- ## More info

- Visit our site [watchit.movie](http://watchit.movie).
- Read our post in [dev.to](https://dev.to/geolffreym/watchit-2b88).
- Get in touch with us in [gitter](https://gitter.im/watchit-app/community).
- For help or bugs please [create an issue](https://github.com/ZorrillosDev/watchit-toolkit/issues). -->

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/phillmac"><img src="https://avatars.githubusercontent.com/u/4534835?v=4?s=100" width="100px;" alt=""/><br /><sub><b>phillmac</b></sub></a><br /><a href="https://github.com/ZorrillosDev/watchit-gateway/commits?author=phillmac" title="Code">💻</a> <a href="#userTesting-phillmac" title="User Testing">📓</a> <a href="#ideas-phillmac" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-phillmac" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="http://mrh.io"><img src="https://avatars.githubusercontent.com/u/106148?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Mark Robert Henderson</b></sub></a><br /><a href="https://github.com/ZorrillosDev/watchit-gateway/commits?author=aphelionz" title="Code">💻</a> <a href="#ideas-aphelionz" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/EchedeyLR"><img src="https://avatars.githubusercontent.com/u/56733813?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Echedenyan</b></sub></a><br /><a href="#infra-EchedeyLR" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
