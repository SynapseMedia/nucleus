[![Gitter](https://badges.gitter.im/watchit-app/community.svg)](https://gitter.im/watchit-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

# Getting started
* If you don’t have Go, [install it](https://golang.org/doc/install).
* If you don’t have IPFS , [install it](https://github.com/ipfs/go-ipfs#install).
* [Spawn go-ipfs node with docker](https://mrh.io/ipfs_docker/).
* [How to spawn an IPFS node in Node.js](https://mrh.io/2018-01-24-pushing-limits-ipfs-orbitdb/).
* For private networks [How to spawn an IPFS private node and generate swarm key](https://mrh.io/ipfs-private-networks/).



# watchit-gateway
Gateway Watchit Seeder

## How

*Start docker containers and starts movies migration.*
> Run seeder/bootstrap IPFS public node. 
> (Please wait until movies get ready migrated).

`docker-compose up`

# watchit-app

After run migration and expose our node in gateway

Please copy `address` in `hash` file located in your root files directory. This key will be requested on app login.*

