#!/usr/bin/env bash
# Build and push script
cd .
docker build -f Dockerfile . -t $1:$2
docker push $1:$2


