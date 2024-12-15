#!/bin/bash

process=$(ps aux | grep '[j]kbms-ac-checker/main.py')
logfile="$(pwd)/jkbms.log"
main="$(pwd)/main.py"

if [[ -z $process ]]; then
        echo -e "\n$(date +"%Y-%m-%d %T.%N") Process not found. Starting..." >> $logfile
        python3 $main &
fi