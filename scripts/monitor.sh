#!/bin/bash

IPFS_API="api/v0"
DEFAULT_PIN_TIMEOUT="2h"

function _curl ()
{
    if [[ -n "${ENABLE_DEBUG}" ]] || [[ -n "${DEBUG_CURL}" ]]
    then
        curl "${@}"
    else
        curl --silent "${@}"
    fi
    echo
}

function _ipfs ()
{
    ipfs --api="/${IPFS_API_PREFIX}/${IPFS_API_HOST}/tcp/${IPFS_API_PORT}" "${@}"
}

function ipfs.links.info ()
{
    jq -r '.[] | "\(.Type) \(.Hash) \(.Name)"'
}

ipfs.ls ()
{
    local addr
    local addr_encoded
    local url
    local ipfs_gateway


    addr=${1}
    ipfs_gateway=${2:-${IPFS_HTTP_GATEWAY}}

    if [[ -z "${addr}" ]]
    then
        echo "IPFS addr is required" >&2
        return 252
    fi

    if [[ -z "${ipfs_gateway}"  ]]
    then
        echo "IPFS gateway is required" >&2
        return 252
    fi


    addr_encoded=$(rawurlencode "${addr}")

    [[ -n "${ENABLE_DEBUG}" ]] && echo "addr_encoded is ${addr_encoded}" >&2

    url="${ipfs_gateway}/${IPFS_API}/ls?arg=${addr_encoded}"

    [[ -n "${ENABLE_DEBUG}" ]] && echo "URL is ${url}" >&2

    jq -r ".Objects[].Links" < <(_curl "${url}")
}

function ipfs.ls.recursive ()
{
    local addr

    local itemtype
    local itemhash
    local itemname

    addr=${1}

    if [[ -z "${addr}" ]]
    then
        echo "IPFS addr is required" >&2
        return 252
    fi

    echo "$(date) Resolving ${addr}" >&2

    while read -r itemtype itemhash itemname
    do
        [[ -n "${ENABLE_DEBUG}" || -n "${DEBUG_IPFS_ITEMS}" ]] && echo "itemtype=${itemtype} itemhash=${itemhash} itemname=${itemname} addr=${addr}" >&2

        echo "${itemtype}" "${itemhash}" "${addr}/${itemname}" "${itemname}"

        if  (( itemtype == 1 ))
        then
            ipfs.ls.recursive "${addr}/${itemname}"
        fi

    done < <(ipfs.ls "${addr}" | ipfs.links.info)
}

function _ipfs.ls.blocks () {

    local addr
    local blocktype
    local blockhash
    local blockcount

    addr=${1}

    (( blockcount=0 ))
    while read -r blocktype blockhash
    do
        (( blockcount += 1 ))
        echo "${blockhash}"
    done < <(ipfs.ls "${addr}" | ipfs.links.info)

    if (( blockcount == 0))
    then
        echo "${addr} has no child blocks" >&2
        echo "${addr}"
    fi

}

function ipfs.ls.blocks () {
    local addr

    local itemtype
    local itemhash
    local itemname
    local itemaddr
    local itemcount

    addr=${1}

    if [[ -z "${addr}" ]]
    then
        echo "IPFS addr is required" >&2
        return 252
    fi
    (( itemcount=0 ))
    while read -r itemtype itemhash itemaddr itemname
    do
        (( itemcount += 1 ))
        [[ -n "${ENABLE_DEBUG}" || -n "${DEBUG_IPFS_BLOCKS}" ]] && echo "itemtype=${itemtype} itemhash=${itemhash} itemaddr=${itemaddr} itemname=${itemname}" >&2

        if (( itemtype == 2 )) && [[ -n "${itemname}" ]]
        then
            echo "$(date) Fetching blocks for ${itemhash} ${itemaddr}" >&2
            _ipfs.ls.blocks "${itemhash}"

        elif (( itemtype == 2 )) && [[ -z "${itemname}" ]]
        then
            echo "${itemhash}"
        fi

    done < <(ipfs.ls.recursive "${addr}")

    if (( itemcount == 0 ))
    then
        echo "${addr} has no items" >&2
        _ipfs.ls.blocks "${addr}"
    fi
}

function curljsonp ()
{
    _curl  -X POST -H "Content-Type: application/json" "${@}"
}

function prune_cid ()
{
    sed 's/\/ipfs\///g' /dev/stdin
}

function ipfs_resolve () {
    local ipns
    local resolve_timeout

    ipns=${1:-$IPNS_RESOLVE_ADDR}
    resolve_timeout=${2:-$IPFS_RESOLVE_TIMEOUT}

    if [[ -z "${ipns}" ]]
    then
	    echo "IPNS_RESOLVE_ADDR is required" >&2
        return 252
    fi

    if [[ -z "${resolve_timeout}" ]]
    then
	    echo "IPFS_RESOLVE_TIMEOUT is required" >&2
        return 252
    fi

    _ipfs resolve "${ipns}" --timeout "${resolve_timeout}"

}

function ipfs_cat () {
    local cat_addr
    local cat_timeout

    cat_addr=${1:-$IPFS_CAT_ADDR}
    cat_timeout=${2:-$IPFS_CAT_TIMEOUT}


    if [[ -z "${cat_addr}" ]]
    then
	    echo "IPFS_CAT_ADDR is required" >&2
        return 252
    fi

    if [[ -z "${cat_timeout}" ]]
    then
	    echo "IPFS_CAT_TIMEOUT is required" >&2
        return 252
    fi

    _ipfs cat --timeout="${cat_timeout}" "${cat_addr}"  && echo
}

function ipfs_cid_format () {
    _ipfs cid format -b base58btc "${1}"
}


function getIPNSBase58BTC()
{
    local resolved
    local ipns
    ipns=${1:-$IPNS_RESOLVE_ADDR}

    if [[ -z "${ipns}" ]]
    then
	    echo "IPNS_RESOLVE_ADDR is required" >&2
        return 252
    fi

    resolved=$(ipfs_resolve "${ipns}" | prune_cid)
    ipfs_cid_format "${resolved}"
}

function rawurlencode ()
{
  local string="${1}"
  local strlen=${#string}
  local encoded=""
  local pos c o

  for (( pos=0 ; pos<strlen ; pos++ ))
  do
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
    local host
    local dbAddr

    host=${2:-${ORBIT_DB_HOST}}

    if [[ -z "${1}" ]]
    then
        echo "DB address is required" >&2
        return 252
    fi

    if [[ -z "${host}" ]]
    then
        echo "Orbit DB host is required" >&2
        return 252
    fi

    dbAddr=$(rawurlencode "${1}")

    if [[ -z "${ORBIT_DB_ENTRIES_TIMEOUT}" ]]
    then
        curljsonp -d "{\"awaitOpen\": false}" "${host}/db/${dbAddr}" | jq
    else
        curljsonp -d "{\"awaitOpen\": false, \"fetchEntryTimeout\": ${ORBIT_DB_ENTRIES_TIMEOUT}}" "${host}/db/${dbAddr}" | jq
    fi
}

function dbs.list.ids ()
{
    local host
    host=${1:-${ORBIT_DB_HOST}}

    if [[ -z "${host}" ]]
    then
        echo "Orbit DB host is required" >&2
        return 252
    fi

    _curl "${host}/dbs" | jq  -r '.[].id'
}

function db.payload.value ()
{
    local host
    local dbAddr
    host=${2:-${ORBIT_DB_HOST}}

    if [[ -z "${1}" ]]
    then
        echo "DB address is required" >&2
        return 252
    fi

    if [[ -z "${host}" ]]
    then
        echo "Orbit DB host is required" >&2
        return 252
    fi

    dbAddr=$(rawurlencode "${1}")
    _curl "${host}/db/${dbAddr}/oplog/values" | jq -r '.[].payload.value'
}

function db.get.contents ()
{
    local host
    local ipfs_gateway
    local entry
    local blockhash

    host=${2:-${ORBIT_DB_HOST}}
    ipfs_gateway=${3:-${IPFS_HTTP_GATEWAY}}

    if [[ -z "${host}"  ]]
    then
        echo "Orbit DB host is required" >&2
        return 252
    fi

    if [[ -z "${ipfs_gateway}"  ]]
    then
        echo "IPFS gateway is required" >&2
        return 252
    fi

    db.payload.value "${1}" "${host}" | while read -r entry
    do
        echo "$(date) Fetching blocks for entry ${entry}" >&2
        while read -r blockhash
        do
            echo "$(date) Fetching block ${blockhash}" >&2
            url="${ipfs_gateway}/${IPFS_API}/dag/get?arg=${blockhash}"
            [[ -n "${ENABLE_DEBUG}" ]] && echo "URL is ${url}" >&2
            _curl "${url}" > /dev/null
        done < <(ipfs.ls.blocks "${entry}")
    done
}

function fetch_all_dbs_contents ()
{
    local host
    host=${1:-${ORBIT_DB_HOST}}

    if [[ -z "${host}"  ]]
    then
        echo "Orbit DB host is required" >&2
        return 252
    fi

    dbs.list.ids "${host}" | while read -r dbaddr
    do
        echo "Fetching DBAddr: ${dbaddr}"
        db.get.contents "${dbaddr}"
    done
}

function resolve_ipns_db ()
{
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

    echo "$(date) Resolving entry ${db_key}" >&2

    db_key_resolved=$(getIPNSBase58BTC "/ipns/${db_key}")

    echo "${db_key_resolved}/${db_name}"
}

function open_ipns_dbs ()
{
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

    echo "$(date) Fetching ipns key listing" >&2

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
            echo "$(date) Resolve failed" >&2
            return 254
        fi

        last_db_addr=$(< "/dev/shm/ipns_resolve/${db_entry}")

        if [[ ! "${last_db_addr}" == "${db_addr}" ]]
        then
            if [[ -n "${db_addr}" ]]
            then
                echo "$(date) Opening ${db_addr}" >&2
                db.open "${db_addr}"
                echo "${db_addr}" > "/dev/shm/ipns_resolve/${db_entry}"
                date
                sleep 30s
                [[ -n "${OPEN_FETCH_DB_CONTENTS}" ]] && db.get.contents "${db_addr}"
            else
            echo "Unable to resolve addr for ${db_entry}" >&2
            fi
            date
        fi


    done < <(ipfs_cat "/ipns/${ipns_key}")
}

function ipfs_pubsub_subscribe () {
    local topic
    local existing_pid

    topic=${1:-${PUBSUB_TOPIC}}

    if [[ -z "${topic}" ]]
    then
        echo "Pubsub topic is required" >&2
        return 252
    fi

    [[ ! -d /dev/shm/pubsub_topics ]] && mkdir -v /dev/shm/pubsub_topics

    if [[ -f  "/dev/shm/pubsub_topics/${topic}" ]]
    then
        existing_pid=$( < "/dev/shm/pubsub_topics/${topic}" )
    fi

    if [[ -z "${existing_pid}" ]] || [[ -n "${existing_pid}" ]] && ! kill -0 "${existing_pid}" > /dev/null 2>&1
    then
        echo "$(date) Subscribing to ${topic}" >&2
        echo "$BASHPID" > "/dev/shm/pubsub_topics/${topic}"
        while :
        do
            _ipfs pubsub sub "${topic}" > /dev/null
            sleep 30
        done
    else
        echo "Already subscribed to ${topic} with pid ${existing_pid}" >&2
    fi
}

function open_ipns_pubsub ()
{
    local ipns_key
    local pubsub_entry
    local pubsub_topic
    local last_pubsub_topic

    ipns_key=${1:-${IPNS_PUBSUB_KEY}}

    if [[ -z "${ipns_key}" ]]
    then
        echo "IPNS key is required" >&2
        return 252
    fi

    echo "$(date) Fetching ipns key listing" >&2

    while read -r pubsub_entry
    do
        if [[ -z "${pubsub_entry}" ]]
        then
            continue
        fi

        daemon /scripts/pubsub-subscribe.sh "${pubsub_entry}"
        date

    done < <(ipfs_cat "/ipns/${ipns_key}")
}

function open_resolve_ipns_pubsub ()
{
    local ipns_key
    local pubsub_entry
    local pubsub_topic
    local last_pubsub_topic

    ipns_key=${1:-${IPNS_PUBSUB_KEY}}

    if [[ -z "${ipns_key}" ]]
    then
        echo "IPNS key is required" >&2
        return 252
    fi

    echo "$(date) Fetching ipns key listing" >&2

    [[ ! -d /dev/shm/ipns_resolve ]] && mkdir -v /dev/shm/ipns_resolve

    while read -r pubsub_entry
    do
        if [[ -z "${pubsub_entry}" ]]
        then
            continue
        fi

       pubsub_topic=$(ipfs_resolve "${pubsub_entry}")

        if [[ -z "${pubsub_topic}" ]]
        then
            echo "$(date) Resolve failed" >&2
            return 254
        fi

        last_pubsub_topic=$(< "/dev/shm/ipns_resolve/${pubsub_topic}")

        if [[ ! "${last_pubsub_topic}" == "${pubsub_topic}" ]]
        then
            daemon /scripts/pubsub-subscribe.sh "${pubsub_entry}"
            date
        fi


    done < <(ipfs_cat "/ipns/${ipns_key}")
}

function monitor_ipns_dbs ()
{
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

    while :
    do
        sleep "${db_wait}" &
        open_ipns_dbs "${monitor_ipns}"
        wait
    done
}

function monitor_ipns_pubsub ()
{
    local monitor_ipns
    local db_wait

    monitor_ipns=${1:-${PUBSUB_MONITOR_IPNS}}
    pubsub_wait=${2:-${PUBSUB_MONITOR_WAIT}}

    if [[ -z "${monitor_ipns}" ]]
    then
        echo "IPNS key is required" >&2
        return 252
    fi

    if [[ -z "${pubsub_wait}" ]]
    then
        echo "Wait duration is required" >&2
        return 252
    fi
    [[ ! -d /var/log ]] && mkdir -v /var/log
    while :
    do
        sleep "${pubsub_wait}" &
        open_ipns_pubsub "${monitor_ipns}"
        wait
    done
}

function ipfs.pin.recursive ()
{
    local ipfs_pin_addr
    local path_filter
    local pin_timeout

    ipfs_pin_addr=${1:-$IPFS_PIN_ADDR}
    path_filter=${2:-${ipfs_pin_addr}/.*/}
    pin_timeout=${IPFS_PIN_TIMEOUT:-${DEFAULT_PIN_TIMEOUT}}

    if [[ -z "${ipfs_pin_addr}" ]]
    then
        echo "IPFS pin addr is required" 1>&2
        return 252
    fi

    while read -r itemhash pathname
    do
        echo "$(date) Pinning folder ${pathname}" 1>&2
        _ipfs pin add --progress --timeout "${pin_timeout}" "${itemhash}"
    done < <(ipfs.ls.recursive.dirs.filtered "${ipfs_pin_addr}" "${path_filter}")
}

function ipfs.ls.recursive.dirs.filtered ()
{
    local filter
    local addr

    addr=${1:-$IPFS_ADDR}
    filter=${2:-$IPFS_FILTER}

    if [[ -z "${addr}" ]]
    then
        echo "IPFS addr is required" 1>&2
        return 252;
    fi

    if [[ -z "${filter}" ]]
    then
        echo "IPFS filter is required" 1>&2
        return 252
    fi

    echo "Filter is ${filter}" 1>&2

    ipfs.ls.recursive.dirs "${addr}" | grep --color=auto "${filter}"
}

function ipfs.ls.recursive.dirs ()
{
    local itemtype
    local itemhash
    local itemname

    echo "$(date) Resolving ${*}" 1>&2;

    while read -r itemtype itemhash itemname
    do
        if (( itemtype == 1))
        then
            echo "${itemhash}" "${1}/${itemname}"
            ipfs.ls.recursive.dirs "${1}/${itemname}"
        fi
    done < <(ipfs.ls "${*}" | ipfs.links.info)
}


export -f ipfs.ls
export -f ipfs.links.info
export -f ipfs.ls.recursive.dirs
export -f ipfs.ls.recursive.dirs.filtered
export -f ipfs.pin.recursive
export -f ipfs_pubsub_subscribe
