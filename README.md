# Watchit Gateway

[![Gitter](https://badges.gitter.im/watchit-app/community.svg)](https://gitter.im/watchit-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

## Getting started

* [Spawn go-ipfs node with docker](https://mrh.io/ipfs_docker/).
* [How to spawn an IPFS node in Node.js](https://mrh.io/2018-01-24-pushing-limits-ipfs-orbitdb/).
* For private networks [How to spawn an IPFS private node and generate swarm key](https://mrh.io/ipfs-private-networks/).

## Quick summary

The watchit gateway is an interface or micro framework for the migration of content to IPFS and the distribution of
metadata through [OrbitDB](https://orbitdb.org/).

Watchit gateway adds migrated data to the metastore (orbitdb) which is distributed in a predefined scheme definition to
ensure the integrity of the data that is later consumed by the [dapp](https://github.com/ZorrillosDev/watchit-desktop).
Watchit gateway provides simple tools for the generation and fetching of content.

## Concepts
Please see our concepts full documentation to understand better the underneath:
* [SCHEME.md](https://github.com/ZorrillosDev/watchit-gateway/blob/master/SCHEME.md)
* [RESOLVERS.md](https://github.com/ZorrillosDev/watchit-gateway/blob/master/RESOLVERS.md)

## Usage
See [USAGE.md](https://github.com/ZorrillosDev/watchit-gateway/blob/master/USAGE.md) for the full documentation.

## Run
1) Copy your custom module resolver to `resolvers` directory.
2) Start container `docker-compose up` to run migrator.
3) After finishing the migration process you can get the orbit addresses.
4) Copy the orbit address and use it when starting the [dapp](https://github.com/ZorrillosDev/watchit-desktop).





