# Watchit Toolkit

[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
[![Gitter](https://badges.gitter.im/watchit-app/community.svg)](https://gitter.im/watchit-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![CI](https://github.com/ZorrillosDev/watchit-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ZorrillosDev/watchit-toolkit/actions/workflows/ci.yml)

> Node, SDK, CLI and REST API for Watchit.

***NOTE!*** The toolkit is **alpha-stage** software. It means toolkit hasn't been security audited and programming APIs and data formats can still change.

The design so far contains 3 layers of abstraction:

1. **The Core**: "The building block" packages here are intended to have minimal or no dependencies, those that have dependencies will be with the same internal packages and as far as possible they will be utility packages.

2. **The SDK**: Exposes the API to the client at the programming level to use core functions in a safe and conformant way.

3. **The CLI and HTTP API**: These make use of the sdk to form the services.

Toolkit its a low level compilation of "toolchain" for Watchit environment.
It includes:

- Metadata harvesting
- Multimedia processing
- Multimedia storage
- Metadata distribution
- Web3 instruments

## Summary

The toolkit proposes a sequence of steps (pipeline) for the processing and decentralization of multimedia:

1. **Harvesting**: collect movies metadata
2. **Processing**: video transcoding and image processing
3. **Schematization**: metadata standard schematization eg. ERC1155 metadata
4. **Storage**: structured storage in the IPFS decentralized network
5. **Blockchain**: mint movies to web3 as NFT
6. **Expose**: distribution of metadata through [OrbitDB](https://orbitdb.org/)

## Terms and Concepts

### Node

In a Nutshell Toolkit itself exposes a node that powers the Watchit network through distributed storage, metadata resolution, reward system and access controls.

The nodes will be rewarded through the IPFS [bitswap](https://docs.ipfs.tech/concepts/bitswap/) which will determine the amount of data provided by each participant, based on this WVT coin will be granted.

The information shared between the nodes will be the assets and movies added to IPFS within the Watchit network, it is important to note that this data will not be stored by default and only those that are requested from the network or those with which you want to feed your node to increase your rewards since the more data you have to share the more rewards you will get.

The nodes will also be facilitators of metadata for the network, each node will have a process that will "pin" with lists of metadata from the different participants in the network (this metadata will be previously encrypted) that will be obtained through the Distribution contract.

It is worth noting that the IPFS nodes running within the network will be "upgraded" nodes to implement all the features described above. Any suggestion or improvement please submit an issue.

### Harvesting

"The *harvest* process consists of a set of instructions, expressed as a Python class. The toolkit will execute the instructions expressed in those classes to obtain content that then populates the metadata schema." - @aphelionz

Harvest resolvers implement the logic necessary for fetch, preprocessing, cleaning and schematization of data from any available
resource. Based on the following class abstraction we can see the methods required for the development of a resolver:

~~~~
Define your resolvers modules below.
Ex: Each resolver must implement 2 fundamental methods.

class Dummy:
    def __str__(self) -> str:
        return 'Test'

    def __call__(self, scheme, *args, **kwargs):
       """
        Returned meta should be valid scheme
        Process your data and populate scheme struct
        
        :param scheme: MovieScheme object
        :returns: Scheme valid object list ex: {movie1, movie2}
        :rtype Generator[MovieScheme]
        """
        yield data
~~~~

Please see [example](https://github.com/ZorrillosDev/watchit-gateway/blob/master/resolvers/dummy/dummy.py)

## Usage

- [SDK]()
- [CLI]()
- [API]()

## Development

Some available capabilities for dev support:

- **Install**: `make bootstrap`
- **Tests**: `make test`
- **Coverage**: `make coverage`
- **Lint**: `make code-fmt`
- **Lint Fix**: `make fix-coding-style`

Note: Please check [Makefile](https://github.com/geolffreym/watchit-toolkit/Makefile) for more capabilities.  

## More info

- Visit our site [watchitapp.site](http://watchit.movie).
- Read our post in [dev.to](https://dev.to/geolffreym/watchit-2b88).
- Get in touch with us in [gitter](https://gitter.im/watchit-app/community).
- For help or bugs please [create an issue](https://github.com/ZorrillosDev/watchit-toolkit/issues).

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
