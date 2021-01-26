#!/bin/bash

## Usage: worker.sh {IPNS_CID}
#
#- IMPLEMENTATION
#-    author          phillmac
#-    license         GNU General Public License


export IPFS_RESOLVE_TIMEOUT=15m
export ORBIT_DB_ENTRIES_TIMEOUT=1000
export ORBIT_DB_HOST="http://127.0.0.1:3001"

function ipfs (){
   docker run --rm  -e "IPFS_API_PREFIX=ip4" -e "IPFS_API_HOST=127.0.0.1" --net host peelvalley/ipfs-cli "${@}";
}

function rawurlencode () {
  local string="${1}"
  local strlen=${#string}
  local encoded=""
  local pos c o

  for (( pos=0 ; pos<strlen ; pos++ )); do
     c=${string:$pos:1}
     case "$c" in
        [-_.~a-zA-Z0-9] ) o="${c}" ;;
        * )               printf -v o '%%%02x' "'$c"
     esac
     encoded+="${o}"
  done
  echo "${encoded}"
}

function db.open ()
{
    local host;
    local dbAddr;
    host=${2:-${ORBIT_DB_HOST}};
    dbAddr=$(rawurlencode "${1}");
    echo "Opening host ${host}"
    curljsonp -d "{\"awaitOpen\":false, \"fetchEntryTimeout\":${ORBIT_DB_ENTRIES_TIMEOUT}}" "${host}/db/${dbAddr}"
}

function curljsonp () {
    echo "Requesting curl"
    curl --silent -X POST -H "Content-Type: application/json" "${@}"
}

function getIPNSBase58BTC() {
    local cid
    local ipns
    ipns=${1=:$IPNS_RESOLVE_ADDR}

    if [[ -z "${ipns}" ]]
    then
        echo "IPNS_RESOLVE_ADDR is required"
        return 252
    fi

    cid=$(ipfs resolve "${ipns}" --timeout "${IPFS_RESOLVE_TIMEOUT}" | sed 's/\/ipfs\///g' /dev/stdin)
    ipfs cid format -b base58btc "${cid}"
}

echo "Running worker"
echo "$(getIPNSBase58BTC /ipns/QmX9owwQsn6AD8wyZGT8L6rCbdqfuo5de26Ez8Ssze7bjQ)/wt.movies.db"
while true; do db.open "$(getIPNSBase58BTC /ipns/QmX9owwQsn6AD8wyZGT8L6rCbdqfuo5de26Ez8Ssze7bjQ)/wt.movies.db"; sleep 5m; done