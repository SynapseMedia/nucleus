#!/usr/bin/env bash
forever stopall
rm hash
rm clients
rm -rf orbitdb/
ipfs pin ls --type recursive | cut -d' ' -f1 | xargs -n1 ipfs pin rm
ipfs repo gc

forever start resource/orbit/migrate.js false