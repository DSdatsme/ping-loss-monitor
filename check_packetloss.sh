#!/bin/bash

############################
# Prerequisites
# make sure you have sqlite setup

############################
SQLITE_DATABASE_PATH='/tmp/monitor.db'
PING_BIN_PATH=/bin/ping
PING_SOURCE=8.8.8.8

curr_time=$(date +%s)

ping_output_stats=$($PING_BIN_PATH -c 5 $PING_SOURCE | tail -1)          # round-trip min/avg/max/stddev = 5.588/9.902/12.013/2.336 ms
all_results=$(echo $ping_output_stats | awk '{print $4}')           # 5.588/9.902/12.013/2.336

min=$(cut -d'/' -f1 <<<$all_results)
avg=$(cut -d'/' -f2 <<<$all_results)
max=$(cut -d'/' -f3 <<<$all_results)
stddev=$(cut -d'/' -f4 <<<$all_results)

sqlite3 $SQLITE_DATABASE_PATH "insert into packet_latency (epoc,min,avg,max,stddev) values ($curr_time,$min,$avg,$max,$stddev);"
