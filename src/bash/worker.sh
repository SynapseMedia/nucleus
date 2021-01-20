#!/bin/bash

function db.open ()
{
    local host;
    local dbAddr;
    host=${2:-${ORBIT_DB_HOST}};
    dbAddr=$(rawurlencode "${1}");
    curljsonp -d "{\"awaitOpen\": false, \"fetchEntryTimeout\": ${ORBIT_DB_ENTRIES_TIMEOUT}}" "${host}/db/${dbAddr}" | python -m json.tool
}

function curljsonp () {
    curl --silent - -X POST -H "Content-Type: application/json" "${@}"
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

while true; do db.open "$(getIPNSBase58BTC /ipns/QmTVvHkQvQuqoMngDzHy4fmFTBAxqp3PqSMGKKLXa8iTKr)/wt.movies.db"; sleep 5m; done