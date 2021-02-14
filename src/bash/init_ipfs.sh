#!/bin/sh

docker-compose exec watchit_ipfs ipfs config Addresses.Swarm '["/ip4/0.0.0.0/tcp/4001", "/ip4/0.0.0.0/tcp/4002/ws", "/ip6/::/tcp/4001"]' --json
docker-compose exec watchit_ipfs ipfs config Peering.Peers '
[
  { "ID": "QmQ4rndRVi4L2cnZ7aiD6RFfYqQpNdmnmgsZD6mgUu5zZX", "Addrs": ["/ip4/34.220.29.107/tcp/4001"] },
  { "ID": "QmP4wC6pRnkzbPdenAsoT199WctTjcGtuvvoGj89wYDs8u", "Addrs": ["/ip4/34.220.216.205/tcp/4001"] },
  { "ID": "12D3KooWQw3vx2E4FKpL9GHC9BpFya1MXVUFEVBAQVhMDkreCqwF", "Addrs": ["/ip4/185.215.224.79/tcp/4001"] },
  { "ID": "12D3KooWD4Z47R1pnzTxCVQAiTKTHasWU2xTAcffyC38BNKM68yw", "Addrs": ["/ip4/185.215.227.40/tcp/4001"] },
  { "ID": "QmbPFTECrXd7o2HS2jWAJ2CyAckv3Z5SFy8gnEHKxxH52g", "Addrs": ["/ip4/144.172.69.157/tcp/4001"] }
]' --json
docker-compose exec watchit_ipfs ipfs config --bool Swarm.EnableRelayHop false
docker-compose exec watchit_ipfs ipfs config --bool Swarm.EnableAutoRelay true
##docker-compose exec watchit_ipfs ipfs config --bool Discovery.MDNS.Enabled true


