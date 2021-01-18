#!/usr/bin/env bash
# Build and push script
cd .
docker build -f $1 . -t $2:$3
docker push $2:$3


