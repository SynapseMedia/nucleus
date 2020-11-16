# watchit-gateway
Gateway Watchit Seeder



1) docker-compose up
// Migrate movies to mongodb
2) docker-compose exec watchit_migrator bash -c "export PYTHONPATH=$PYTHONPATH:/data/watchit && python resource/py/migrate.py"
3) ipfs init
4) ipfs id # Copy ipfs ID (ex: QmNWCiQTM1drWrdAM5jgRjdGiDoy7sYjznpip1BZU1Jz5m)
5) bash ./resource/bash/init_ipfs.sh {YOUR_IPFS_ID_HERE}
6) ipfs daemon  --enable-pubsub-experiment
7) bash ./resource/bash/restart_ipfs.sh


# watchit-app
In https://github.com/ZorrillosDev/watchit-desktop/blob/master/public/lib/settings/orbit.js set your ENV variables with BOOTSTRAP_IP address (Gateway IP) and BOOTSTRAP_HASH (IPFS ID ex: QmNWCiQTM1drWrdAM5jgRjdGiDoy7sYjznpip1BZU1Jz5m)

