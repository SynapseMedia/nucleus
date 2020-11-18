# watchit-gateway
Gateway Watchit Seeder

## How

*Start docker containers*

1) `docker-compose up`

*Migrate movies to mongodb (Please wait until movies get ready migrated)*

2) `docker-compose exec watchit_migrator bash -c "export PYTHONPATH=$PYTHONPATH:/data/watchit && python resource/py/migrate.py"`

*Initialize IPFS*

3) `ipfs init`

*In a new console please get ID and copy it*

4) `ipfs id # Copy ipfs ID (ex: QmNWCiQTM1drWrdAM5jgRjdGiDoy7sYjznpip1BZU1Jz5m)`

*Now lets get init and set bootstrap ipfs node*

5) `bash ./resource/bash/init_ipfs.sh {YOUR_IPFS_ID_HERE}`

*Run ipfs daemon as background*

6) `ipfs daemon  --enable-pubsub-experiment &`

*And expose our node tu ipfs network migration*

7) `bash ./resource/bash/restart_ipfs.sh`


# watchit-app

*After run migration in gateway*

1) Two file are generated `hash` and `clients`. Please copy first entry hash in `hash` file and any of the list in `clients` file

*To configure your app please*

2) In [this file](https://github.com/ZorrillosDev/watchit-desktop/blob/master/public/lib/settings/orbit.js) set your ENV variables with: `BOOTSTRAP_IP = {GATEWAY_IP} BOOTSTRAP_HASH = {COPIED_ID}`



