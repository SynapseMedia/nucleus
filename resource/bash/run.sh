#!/usr/bin/env bash
sudo npm i -g forever

forever stopall
rm hash
rm -rf orbitdb/

# Fix sort memory error in mongo
docker-compose exec watchit_mongo mongo --eval 'db.adminCommand({setParameter: 1, internalQueryExecMaxBlockingSortBytes:1048576000})' > /dev/null
docker-compose exec watchit_mongo mongo --eval 'db.adminCommand({setParameter: 1, internalQueryMaxBlockingSortMemoryUsageBytes:1048576000})' > /dev/null

# Run migration and expose orbit forever
forever start resource/orbit/migrate.js false