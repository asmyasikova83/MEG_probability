#!/bin/sh

d=`date +"%Y_%m_%d__%H_%M_%S"`

run() {
	MODE=$1
	log_collect=nohup__collect_${MODE}__$d.out
	echo "nohup python -u collect.py full_$MODE < /dev/null &> $log_collect &"
	echo "( to find PID use: ps -aux | grep collect )"
	nohup python -u collect.py full_$MODE < /dev/null >> $log_collect 2>&1 &
	echo "nohup log log_collect_$MODE: $log_collect"
	echo ""
}

run "ERF"
run "TFR"

