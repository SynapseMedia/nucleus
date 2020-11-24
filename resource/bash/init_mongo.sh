#!/usr/bin/env bash
mongo --eval 'db.runCommand({ logRotate : 1 });'
mongo --eval 'db.adminCommand({setParameter: 1, internalQueryExecMaxBlockingSortBytes:1048576000})'
mongo --eval 'db.adminCommand({setParameter: 1, internalQueryMaxBlockingSortMemoryUsageBytes:1048576000})'

