#!/bin/bash 

echo Received: $1
echo Received: $2
echo Received: $3
echo Received: $4

_term() { 
  echo "Caught SIGTERM signal!" 
  kill -TERM "$child" 2>/dev/null
}

trap _term SIGTERM

#source /opt/OpenFOAM/OpenFOAM-v1606+/etc/bashrc
#foamExec "$@" &

sleep 30s &

child=$!
wait "$child"
