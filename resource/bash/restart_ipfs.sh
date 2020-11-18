#!/usr/bin/env bash
forever stopall
rm hash
rm clients
rm -rf orbitdb/

# Clean old pinned data
ipfs pin ls --type recursive | cut -d' ' -f1 | xargs -n1 ipfs pin rm
ipfs repo gc

# Fix sort memory error in mongo
docker-compose exec watchit_mongo mongo --eval 'db.adminCommand({setParameter: 1, internalQueryExecMaxBlockingSortBytes:1048576000})'
docker-compose exec watchit_mongo mongo --eval 'db.adminCommand({setParameter: 1, internalQueryMaxBlockingSortMemoryUsageBytes:1048576000})'

# Run migration and expose orbit forever
forever start resource/orbit/migrate.js false