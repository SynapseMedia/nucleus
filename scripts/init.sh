#!/bin/sh
# shellcheck disable=SC2034
peers=`cat /peering/peers.json`
ipfs init
ipfs config Addresses.Swarm '["/ip4/0.0.0.0/tcp/4001", "/ip4/0.0.0.0/tcp/4002/ws", "/ip6/::/tcp/4001"]' --json
# shellcheck disable=SC2016
ipfs config Peering.Peers "$peers" --json
ipfs config --bool Swarm.EnableRelayHop false
ipfs config --bool Swarm.EnableAutoRelay true
ipfs daemon --migrate=true --enable-gc --enable-namesys-pubsub --enable-pubsub-experiment




