[![Gitter](https://badges.gitter.im/watchit-app/community.svg)](https://gitter.im/watchit-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

# Getting started
* If you don’t have Go, [install it](https://golang.org/doc/install).
* If you don’t have IPFS , [install it](https://github.com/ipfs/go-ipfs#install).
* [Spawm go-ipfs with docker](https://mrh.io/ipfs_docker/).
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

1) After run migration and expose our node in gateway

> Please copy entry hash in `clients` file located in your root files directory and the `private key` as well. This keys will be requested on app login.*

2) To configure your app please go into [this file](https://github.com/ZorrillosDev/watchit-desktop/blob/master/public/lib/settings/ipfs.js) and set your ENV variables.

> Get "IPFS_NODE_ID" using `docker-compose exec watchit_ipfs ipfs id -f=<id>`.

`BOOTSTRAP_LIST=['/ip4/{GATEWAY_IP}/tcp/4001/p2p/{IPFS_NODE_ID}','/ip4/{GATEWAY_IP}/tcp/4002/ws/p2p/{IPFS_NODE_ID}']` 




