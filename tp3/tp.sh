#!/bin/bash

OPTIONS=""
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -e)
    EX_PATH_1="$2"
    shift
    ;;
    -k)
    TAUX="$2"
    shift
    ;;
    -p )
    OPTIONS="${OPTIONS}${1} "
    ;;
    *)
        echo "Argument inconnu: ${1}"
        exit
    ;;
esac
shift
done

python3 ./algorithm.py -e $EX_PATH_1 -k $TAUX $OPTIONS
