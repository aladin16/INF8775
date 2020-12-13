#!/bin/bash

OPTIONS=""
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -a)
    ALGO="$2"
    shift
    ;;
    -e)
    EX_PATH_1="$2"
    shift
    ;;
    -c|-p|-t)
    OPTIONS="${OPTIONS}${1} "
    ;;
    *)
        echo "Argument inconnu: ${1}"
        exit
    ;;
esac
shift
done

python3 ./src/$ALGO.py -e $EX_PATH_1 -a $ALGO $OPTIONS
