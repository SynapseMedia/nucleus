#!/usr/bin/env bash

wget https://golang.org/dl/go1.14.4.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.14.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

wget https://dist.ipfs.io/ipfs-update/v1.6.0/ipfs-update_v1.6.0_linux-amd64.tar.gz
tar -xvf ipfs-update_v1.6.0_linux-amd64.tar.gz
cd ipfs-update && sh install.sh
/usr/local/bin/ipfs-update/ipfs-update install 0.6.0
