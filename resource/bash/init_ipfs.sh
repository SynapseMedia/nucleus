#!/bin/sh
set -e
user=ipfs
repo="$IPFS_PATH"

if [ `id -u` -eq 0 ]; then
  echo "Changing user to $user"
  # ensure folder is writable
  su-exec "$user" test -w "$repo" || chown -R -- "$user" "$repo"
  # restart script with new privileges
  exec su-exec "$user" "$0" "$@"
fi

# 2nd invocation with regular user
ipfs version

if [ -e "$repo/config" ]; then
  echo "Found IPFS fs-repo at $repo"
else
  case "$IPFS_PROFILE" in
    "") INIT_ARGS="" ;;
    *) INIT_ARGS="--profile=$IPFS_PROFILE" ;;
  esac

  ipfs init $INIT_ARGS
  ipfs config Addresses.Swarm '["/ip4/0.0.0.0/tcp/4001", "/ip4/0.0.0.0/tcp/4002/ws", "/ip6/::/tcp/4001", "/ip4/0.0.0.0/udp/4001/quic", "/ip6/::/udp/4001/quic"]' --json
  ipfs config Addresses.API /ip4/0.0.0.0/tcp/5001
  ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080

  # Set up the swarm key, if provided
  SWARM_KEY_FILE="$repo/swarm.key"
  SWARM_KEY_PERM=0400

  # Create a swarm key from a given environment variable
  if [ ! -z "$IPFS_SWARM_KEY" ] ; then
    echo "Copying swarm key from variable..."
    echo -e "$IPFS_SWARM_KEY" >"$SWARM_KEY_FILE" || exit 1
    chmod $SWARM_KEY_PERM "$SWARM_KEY_FILE"
  fi

  # Unset the swarm key variable
  unset IPFS_SWARM_KEY

  # Check during initialization if a swarm key was provided and
  # copy it to the ipfs directory with the right permissions
  # WARNING: This will replace the swarm key if it exists
  if [ ! -z "$IPFS_SWARM_KEY_FILE" ] ; then
    echo "Copying swarm key from file..."
    install -m $SWARM_KEY_PERM "$IPFS_SWARM_KEY_FILE" "$SWARM_KEY_FILE" || exit 1
  fi

  # Unset the swarm key file variable
  unset IPFS_SWARM_KEY_FILE
  ipfs config Datastore.StorageMax 30GB
  ipfs config Datastore.BloomFilterSize 1048576 --json
  ipfs config Swarm.EnableAutoRelay true --json
  ipfs config Swarm.EnableRelayHop true --json
  ipfs config Discovery.MDNS.Enabled true --json # Allowed be found in local

  ipfs bootstrap rm --all
  ipfs bootstrap add /dns4/node0.preload.ipfs.io/tcp/443/wss/p2p/QmZMxNdpMkewiVZLMRxaNxUeZpDUb34pWjZ1kZvsd16Zic
  ipfs bootstrap add /dns4/node1.preload.ipfs.io/tcp/443/wss/p2p/Qmbut9Ywz9YEDrz8ySBSgWyJk41Uvm2QJPhwDJzJyGFsD6
  ipfs bootstrap add /dns4/node2.preload.ipfs.io/tcp/443/wss/p2p/QmV7gnbW5VTcJ3oyM2Xk1rdFBJ3kTkvxc87UFGsun29STS
  ipfs bootstrap add /dns4/node3.preload.ipfs.io/tcp/443/wss/p2p/QmY7JB6MQXhxHvq7dBDh4HpbH29v4yE9JRadAVpndvzySN

  # Get current id
  current_node_id=$(ipfs id -f="<id>")
  ipfs bootstrap add /dns4/watchit_ipfs/tcp/4001/p2p/"$current_node_id"
  ipfs bootstrap add /dns4/watchit_ipfs/tcp/4002/ws/p2p/"$current_node_id"
  ipfs bootstrap add /ip4/0.0.0.0/tcp/4001/p2p/"$current_node_id"
  ipfs bootstrap add /ip4/0.0.0.0/tcp/4002/ws/p2p/"$current_node_id"

  export IPFS_FD_MAX=8192
  ulimit -n 8192

fi

exec ipfs "$@"
