[![Gitter](https://badges.gitter.im/watchit-app/community.svg)](https://gitter.im/watchit-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)


# watchit-gateway
Gateway Watchit Seeder

## How

*Start docker containers and starts movies migration to mongodb (Please wait until movies get ready migrated)*

1) `docker-compose up`

*Initialize IPFS*

2) `ipfs init`

*In a new console please get ID and copy it*

3) `ipfs id # Copy ipfs ID (ex: QmNWCiQTM1drWrdAM5jgRjdGiDoy7sYjznpip1BZU1Jz5m)`

*Now lets get init and set bootstrap ipfs node*

4) `bash ./resource/bash/init_ipfs.sh {YOUR_IPFS_ID_HERE}`

*Run ipfs daemon as background*

5) `ipfs daemon  --enable-pubsub-experiment &`

*And expose our node tu ipfs network over orbitdb migration*

7) `bash ./resource/bash/restart_ipfs.sh`


# watchit-app

*After run migration (Step 2) and expose our node in gateway (Step 7)*

1) `clients` file is generated after this step. Please copy entry hash in `clients` file and corresponding `Private Key`. This keys will be requested on app login. 

*To configure your app please*

2) In [this file](https://github.com/ZorrillosDev/watchit-desktop/blob/master/public/lib/settings/orbit.js) set your ENV variables with: `BOOTSTRAP_IP = {GATEWAY_IP} BOOTSTRAP_HASH = {COPIED_ID}`



