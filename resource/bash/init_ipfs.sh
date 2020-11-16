#https://medium.com/coinmonks/ipfs-production-configuration-57121f0daab2
export IPFS_PATH=~/.ipfs
export EDITOR=vim

my_external_ip=$(dig +short myip.opendns.com @resolver1.opendns.com)
# my_local_ip=$(ip route get 8.8.8.8 | awk -F"src " 'NR==1{split($2,a," ");print a[1]}')

# ipfs init --profile server
# ipfs init
ipfs config Datastore.StorageMax 50GB
ipfs config Datastore.BloomFilterSize 1048576 --json
ipfs config Addresses.Swarm '["/ip4/0.0.0.0/tcp/4001", "/ip4/0.0.0.0/tcp/4002/ws", "/ip6/::/tcp/4001", "/ip4/0.0.0.0/udp/4001/quic", "/ip6/::/udp/4001/quic"]' --json
ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080
ipfs config Addresses.API /ip4/0.0.0.0/tcp/5001
ipfs config Swarm.EnableAutoRelay true --json
ipfs config Swarm.EnableRelayHop true --json
ipfs config Discovery.MDNS.Enabled false --json

ipfs bootstrap rm --all
ipfs bootstrap add /dns4/node0.preload.ipfs.io/tcp/443/wss/p2p/QmZMxNdpMkewiVZLMRxaNxUeZpDUb34pWjZ1kZvsd16Zic
ipfs bootstrap add /dns4/node1.preload.ipfs.io/tcp/443/wss/p2p/Qmbut9Ywz9YEDrz8ySBSgWyJk41Uvm2QJPhwDJzJyGFsD6
ipfs bootstrap add /dns4/node2.preload.ipfs.io/tcp/443/wss/p2p/QmV7gnbW5VTcJ3oyM2Xk1rdFBJ3kTkvxc87UFGsun29STS
ipfs bootstrap add /dns4/node3.preload.ipfs.io/tcp/443/wss/p2p/QmY7JB6MQXhxHvq7dBDh4HpbH29v4yE9JRadAVpndvzySN

ipfs bootstrap add /ip4/"$my_external_ip"/tcp/4001/p2p/$1
ipfs bootstrap add /ip4/"$my_external_ip"/tcp/4002/ws/p2p/$1
ipfs bootstrap add /ip4/0.0.0.0/tcp/4001/p2p/$1
ipfs bootstrap add /ip4/0.0.0.0/tcp/4002/ws/p2p/$1

export IPFS_FD_MAX=8192
ulimit -n 8192

#ipfs daemon  --enable-pubsub-experiment
