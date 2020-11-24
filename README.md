[![Gitter](https://badges.gitter.im/watchit-app/community.svg)](https://gitter.im/watchit-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

# Getting started
* If you don’t have Go, [install it](https://golang.org/doc/install).
* If you don’t have IPFS , [install it](https://github.com/ipfs/go-ipfs#install).
* Look [into this example](https://mrh.io/2018-01-24-pushing-limits-ipfs-orbitdb/) how to spawn an IPFS node in Node.js and in the Browser
* Look [into this example](https://mrh.io/ipfs-private-networks/) how to spawn an IPFS private node and generate swarm key



# watchit-gateway
Gateway Watchit Seeder

## How

*Start docker containers and starts movies migration to mongodb (Please wait until movies get ready migrated)*

1) `docker-compose up`

*Now lets get init and set bootstrap ipfs node. Run ipfs daemon as background and expose our node tu ipfs network with orbitdb migration*

2) `bash ./resource/bash/run.sh {DB_VERSION_DATE ex: format YYMMDD (20201124)}`

# watchit-app

*After run migration and expose our node in gateway *

1) `clients` file is generated . Please copy entry hash in `clients` file and corresponding `private key`. This keys will be requested on app login. 

*To configure your app please*

2) In [this file](https://github.com/ZorrillosDev/watchit-desktop/blob/master/public/lib/settings/orbit.js) set your ENV variables with: 
Get ipfs "node id" using `docker-compose exec watchit_ipfs ipfs id -f=<id>`
* `BOOTSTRAP_IP = {GATEWAY_IP} `
* `BOOTSTRAP_HASH = {IPFS_NODE_ID}`



