#!/bin/sh
ipfs config Addresses.Swarm '["/ip4/0.0.0.0/tcp/4001", "/ip4/0.0.0.0/tcp/4002/ws", "/ip6/::/tcp/4001"]' --json
ipfs config Peering.Peers '
[
  { "ID": "QmSHSTNyKJ1EGVVKj7dKZFmxj9FaBfE7S23MNTj1Jwungg", "Addrs": ["/ip4/34.209.228.155/tcp/4001"] },
  { "ID": "12D3KooWQw3vx2E4FKpL9GHC9BpFya1MXVUFEVBAQVhMDkreCqwF", "Addrs": ["/ip4/185.215.224.79/tcp/4001"] },
  { "ID": "12D3KooWD4Z47R1pnzTxCVQAiTKTHasWU2xTAcffyC38BNKM68yw", "Addrs": ["/ip4/185.215.227.40/tcp/4001"] },
  { "ID": "QmbPFTECrXd7o2HS2jWAJ2CyAckv3Z5SFy8gnEHKxxH52g", "Addrs": ["/ip4/144.172.69.157/tcp/4001"] }
]' --json
ipfs config --bool Swarm.EnableRelayHop false
ipfs config --bool Swarm.EnableAutoRelay true
ipfs daemon --migrate=true --enable-gc --enable-namesys-pubsub



