#!/usr/bin/env bash
rm hash
rm client
rm -rf orbitdb/
forever stopall
forever start resource/orbit/migrate.js $1 $2