#!/bin/bash

function _curl () {
    curl --silent "${@}"
    echo
}

function _ipfs () {
    ipfs --api="/${IPFS_API_PREFIX}/${IPFS_API_HOST}/tcp/${IPFS_API_PORT}" "${@}"
}

function curljsonp () {
    _curl  -X POST -H "Content-Type: application/json" "${@}"
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

    cid=$(_ipfs resolve "${ipns}" --timeout "${IPFS_RESOLVE_TIMEOUT}" | sed 's/\/ipfs\///g' /dev/stdin)
    _ipfs cid format -b base58btc "${cid}"
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

function db.open () {
    local host
    local dbAddr

    host=${2:-${ORBIT_DB_HOST}}

    dbAddr=$(rawurlencode "${1}")

    curljsonp -d "{\"awaitOpen\": false, \"fetchEntryTimeout\": ${ORBIT_DB_ENTRIES_TIMEOUT}}" "${host}/db/${dbAddr}" | jq
}

function resolve_ipns_db () {
    local db_key
    local db_name
    local db_key_resolved

    db_key=${1}
    db_name=${2:-${IPNS_DB_NAME}}

    if [[ -z "${db_key}" ]]
    then
        echo "DB key is required" >&2
        return 252
    fi

    echo "Resolving entry ${db_key}" >&2

    db_key_resolved=$(getIPNSBase58BTC "/ipns/${db_key}")

    echo "${db_key_resolved}/${db_name}"
}

function open_ipns_dbs () {
    local ipns_key
    local db_entry
    local db_addr
    local last_db_addr

    ipns_key=${1:-${IPNS_DBS_KEY}}

    if [[ -z "${ipns_key}" ]]
    then
        echo "IPNS key is required" >&2
        return 252
    fi

    echo "Fetching ipns key listing" >&2

    [[ ! -d /dev/shm/ipns_resolve ]] && mkdir -v /dev/shm/ipns_resolve

    while read -r db_entry
    do
        if [[ -z "${db_entry}" ]]
        then
            continue
        fi

       db_addr=$(resolve_ipns_db "${db_entry}")

        if [[ -z "${db_addr}" ]]
        then
            echo "Resolve failed" >&2
            return 254
        fi

        last_db_addr=$(< "/dev/shm/ipns_resolve/${db_entry}")

        if [[ ! "${last_db_addr}" == "${db_addr}" ]]
        then
            echo "Opening ${db_addr}" >&2
            db.open "${db_addr}"
            echo "${db_addr}" > "/dev/shm/ipns_resolve/${db_entry}"
            date
        fi


    done < <(_ipfs cat --timeout="${IPFS_CAT_TIMEOUT}" "/ipns/${ipns_key}")
}

function monitor_ipns_dbs () {
    local monitor_ipns
    local db_wait

    monitor_ipns=${1:-${DB_MONITOR_IPNS}}
    db_wait=${1:-${DB_MONITOR_WAIT}}

    if [[ -z "${monitor_ipns}" ]]
    then
        echo "IPNS key is required" >&2
        return 252
    fi

    if [[ -z "${db_wait}" ]]
    then
        echo "Wait duration is required" >&2
        return 252
    fi

    while true
    do
        sleep "${db_wait}" &
        open_ipns_dbs "${monitor_ipns}"
        wait
    done
}


