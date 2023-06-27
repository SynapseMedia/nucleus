# Nucleus

[![Slack](https://camo.githubusercontent.com/552ad37eb845d5e54e1bef55f3ea7adb185f36c845a6b676eec85e97122b2fcd/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f736c61636b2d6a6f696e2d6f72616e67652e737667)](https://join.slack.com/t/synapse-media/shared_invite/zt-1vbnai6ee-zxOs1Outt2oGMA7Sh1CXgQ)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![CI](https://github.com/ZorrillosDev/watchit-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ZorrillosDev/watchit-toolkit/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/SynapseMedia/nucleus/branch/main/graph/badge.svg?token=M9FF5B6UNA)](https://codecov.io/gh/SynapseMedia/nucleus)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

***NOTE!*** Nucleus is **alpha-stage** software. It means nucleus hasn't been security audited and programming APIs and data formats can still change.

Nucleus is a collection of low-level tools for decentralized media management, that simplifies the processing, storage, and distribution of multimedia. Its key features include:

1. **Metadata harvesting**: Simplify the extraction and collection of metadata associated with multimedia resources.
2. **Multimedia processing**: Robust tools for processing multimedia content, including transcoding and image manipulation.
3. **Multimedia storage**: Enables secure and efficient storage of multimedia files within the IPFS ecosystem.
4. **Metadata distribution**: Facilitates seamless distribution of metadata across federated networks.
5. **Web3 instruments**: Integrates with Web3 technologies, leveraging blockchain and smart contracts.

## Help

See [documentation](https://synapsemedia.github.io/nucleus/) for more details.

## Installing

Try nucleus! Install is simple using pip: `pip install nucleus-sdk`

Before using `nucleus`, FFmpeg and IPFS must be installed:

- Check the official docs to [install IPFS](https://docs.ipfs.tech/install/command-line/#system-requirements).
- There are a variety of ways to install FFmpeg, such as the [official download links](https://ffmpeg.org/download.html), or using your package manager of choice (e.g. `sudo apt install ffmpeg` on Debian/Ubuntu, `brew install ffmpeg` on OS X, etc.).

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

## More info

- Check our roadmap at [synapsemedia.io](https://synapsemedia.io)
- Follow us on [twitter](https://twitter.com/synapse__media) | [reddit](https://www.reddit.com/r/synapse_media/)
- Get in touch with us on [slack](https://join.slack.com/t/synapse-media/shared_invite/zt-1vbnai6ee-zxOs1Outt2oGMA7Sh1CXgQ) | [discord](https://discord.gg/YW2RmGJ9YF)
- For help or reporting bugs, please create an [issue](https://github.com/SynapseMedia/nucleus/issues).
