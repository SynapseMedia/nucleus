# Watchit Toolkit (WIP)
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
[![Gitter](https://badges.gitter.im/watchit-app/community.svg)](https://gitter.im/watchit-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Test](https://github.com/ZorrillosDev/watchit-toolkit/actions/workflows/test.yml/badge.svg)](https://github.com/ZorrillosDev/watchit-toolkit/actions/workflows/test.yml)

## Getting started
* [Spawn go-ipfs node with docker](https://mrh.io/ipfs_docker/).
* [How to spawn an IPFS node in Node.js](https://mrh.io/2018-01-24-pushing-limits-ipfs-orbitdb/).
* For private networks [How to spawn an IPFS private node and generate swarm key](https://mrh.io/ipfs-private-networks/).

## Quick summary
***NOTE!*** The gateway is **alpha-stage** software. It means watchit-gateway hasn't been security audited and programming APIs and data formats can still change.

The watchit gateway is an interface or micro framework for the migration of content to IPFS and the distribution of
metadata through [OrbitDB](https://orbitdb.org/).

Watchit gateway adds migrated data to the metastore (orbitdb) which is distributed in a predefined scheme to
ensure the integrity of the data that is later consumed by the [dapp](https://github.com/ZorrillosDev/watchit-desktop).
Watchit gateway provides simple tools for the generation and fetching of content.

### Resolvers

"A _resolver_ is a set of instructions, expressed as a Python class. A _gateway_ will execute a resolver to fetch
content from various sources that later populate the schema." - @aphelionz

Resolvers implement the logic necessary for fetch, preprocessing, cleaning and schematization of data from any available
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
        src/core/scheme/definition.py
        
        :param scheme: MovieScheme object
        :returns: Scheme valid object list ex: {movie1, movie2}
        :rtype Generator[MovieScheme]
        """
        yield data
~~~~

Please see [example](https://github.com/ZorrillosDev/watchit-gateway/blob/master/resolvers/dummy/dummy.py)

### Scheme and Usage

* [SCHEME.md](https://github.com/ZorrillosDev/watchit-gateway/blob/master/SCHEME.md).

* [USAGE.md](https://github.com/ZorrillosDev/watchit-gateway/blob/master/USAGE.md).


## Development
 Please make sure you have `make` installed. Please see instructions for [windows](http://gnuwin32.sourceforge.net/packages/make.htm) install.

### Install
`make bootstrap` to install dependencies

### Test

In the project directory, you can run:

`make test` to run code test and `make test-coverage` to check code coverage

### Lint

In the project directory, you can run:
`make` to run linter or `make fix-coding-style` to fix linting


##  More info
* Visit our site [watchitapp.site](http://watchitapp.site).
* Read our post in [dev.to](https://dev.to/geolffreym/watchit-2b88).
* Check out [the roadmap](https://github.com/ZorrillosDev/watchit-gateway/projects/1) to future features.
* Get in touch with us in [gitter](https://gitter.im/watchit-app/community).
* For help or bugs please [create an issue](https://github.com/ZorrillosDev/watchit-gateway/issues).


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
