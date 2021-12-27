#!/bin/sh

# shellcheck disable=SC2006
peers=`cat /peering/peers.json`
[ ! -e "/ipfsdata/config" ] && ipfs init --empty-repo --profile badgerds
ipfs config Addresses.Swarm '["/ip4/0.0.0.0/tcp/4001", "/ip4/0.0.0.0/tcp/4002/ws", "/ip6/::/tcp/4001"]' --json
ipfs config Addresses.API '/ip4/0.0.0.0/tcp/5001'
ipfs config Addresses.Gateway '/ip4/0.0.0.0/tcp/8080'
# shellcheck disable=SC2016
ipfs config Peering.Peers "$peers" --json
ipfs config Swarm.AddrFilters '[
       "/ip4/100.64.0.0/ipcidr/10",
       "/ip4/169.254.0.0/ipcidr/16",
       "/ip4/198.18.0.0/ipcidr/15",
       "/ip4/198.51.100.0/ipcidr/24",
       "/ip4/203.0.113.0/ipcidr/24",
       "/ip4/240.0.0.0/ipcidr/4",
       "/ip6/100::/ipcidr/64",
       "/ip6/2001:2::/ipcidr/48",
       "/ip6/2001:db8::/ipcidr/32",
       "/ip6/fc00::/ipcidr/7",
       "/ip6/fe80::/ipcidr/10"
]' --json


ipfs config Datastore.GCPeriod "24h"
ipfs config Datastore.StorageMax "1000GB"
ipfs config Datastore.StorageGCWatermark 99 --json
ipfs config Pubsub.Router "gossipsub"
ipfs config --json Swarm.DisableBandwidthMetrics false
ipfs daemon --migrate=true --enable-gc --enable-pubsub-experiment --enable-namesys-pubsub

