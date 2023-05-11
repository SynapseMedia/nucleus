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
4. **Expose**: metadata imprinted onto Blocks/IPLD
5. **Mint**: mint meta as NFTs
6. **Retrieval**: unmarshall and distribution of metadata

The pipeline design was based on the decoupling principle, allowing for different use cases. For instance, some elements such as the **storage** component may be optional if data is already stored on the IPFS network, or the **mint** component may be optional if there is no need to create NFTs for the metadata. Similarly, the **processing** component may not be necessary if the media is ready for storage.

"Retrieval" is an auxiliary component that allows for the retrieval and unmarshalling of data from meta lake as raw information that can then be used for distribution through any available or preferred means. In our case, we use Orbit as a distributed ledger for the "out of the box" consumption of our metadata.

## Installing

Before using `nucleus`, FFmpeg and IPFS must be installed.

1) Check the official docs to [install IPFS](https://docs.ipfs.tech/install/command-line/#system-requirements).
2) There are a variety of ways to install FFmpeg, such as the [official download links](https://ffmpeg.org/download.html), or using your package manager of choice (e.g. `sudo apt install ffmpeg` on Debian/Ubuntu, `brew install ffmpeg` on OS X, etc.).

## Examples

- [Full Pipeline](./examples/full.py)

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
