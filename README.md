# Nucleus

[![Slack](https://camo.githubusercontent.com/552ad37eb845d5e54e1bef55f3ea7adb185f36c845a6b676eec85e97122b2fcd/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f736c61636b2d6a6f696e2d6f72616e67652e737667)](https://join.slack.com/t/synapse-media/shared_invite/zt-1vbnai6ee-zxOs1Outt2oGMA7Sh1CXgQ)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![CI](https://github.com/ZorrillosDev/watchit-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ZorrillosDev/watchit-toolkit/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/SynapseMedia/nucleus/branch/main/graph/badge.svg?token=M9FF5B6UNA)](https://codecov.io/gh/SynapseMedia/nucleus)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

***NOTE!*** Nucleus is **alpha-stage** software. It means nucleus hasn't been security audited and programming APIs and data formats can still change.

Nucleus is a collection of low-level tools for media decentralization. It offers functionalities to make it easier to process, store, and distribute multimedia in a decentralized way.

The key features of Nucleus include:

- **Metadata harvesting**
- **Multimedia processing**
- **Multimedia storage**
- **Metadata distribution**
- **Web3 instruments**

Nucleus follows a modular and layered design approach:

1. **The Core**: This layer contains the building block packages that have minimal or no external dependencies. Any dependencies within the core layer will be limited to other internal packages.

2. **The SDK**: The SDK exposes the programming-level API to interact with the core functions in a safe and conformant way.

3. **The CLI and HTTP API**: These components utilize the SDK to provide services through command-line interfaces (CLI) and HTTP API endpoints.

## Summary

Nucleus proposes a sequence of steps (pipeline) for the processing and decentralization of multimedia:

1. **Harvesting**: Collect metadata associated with the multimedia content.
2. **Processing**: Performing media processing tasks.
3. **Storage**:  Store the processed content in the IPFS network.
4. **Expose**: Distribute metadata through the IPFS ecosystem.
5. **Mint**: Create metadata as NFTs (Non-Fungible Tokens).
6. **Retrieval**: Facilitates the retrieval and unmarshalling of metadata from IPFS ecosystem.

The pipeline is modular and adheres to the decoupling principle, enabling flexible use cases. For instance, the **storage** component can be optional if data is already stored on the IPFS network. Similarly, the **mint** component can be skipped if there is no need to create NFTs for the metadata. The **processing** component may also be unnecessary if the media is already prepared for storage.

As part of the metadata federation, **Meta Lake** emerges as a new concept in the Nucleus ecosystem, referring to the central communication point for metadata distribution. The [serialization](https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md) process of the metadata determines the transmission medium, with IPLD and Raw Blocks being among the means used by Nucleus. You can find more information about serialization in the following link:

## Installing

Try nucleus! Install is simple using pip: `pip install nucleus-sdk`

Before using `nucleus`, FFmpeg and IPFS must be installed.

1) Check the official docs to [install IPFS](https://docs.ipfs.tech/install/command-line/#system-requirements).
2) There are a variety of ways to install FFmpeg, such as the [official download links](https://ffmpeg.org/download.html), or using your package manager of choice (e.g. `sudo apt install ffmpeg` on Debian/Ubuntu, `brew install ffmpeg` on OS X, etc.).

## Examples

- [Full Pipeline](./examples/full.py)

## Development

Some available capabilities for dev support:

- **Install**: `make install`
- **Tests**: `make test`
- **Debug**: `make debug`
- **Lint**: `make lint`
- **Lint Fix**: `make format`

Note: Run `make help` to check for more capabilities.  
