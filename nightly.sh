#!/bin/sh

d=`date +"%Y_%m_%d__%H_%M_%S"`

run() {
	MODE=$1
	log_full=nohup__full_${MODE}__$d.out
	echo "nohup python -u nightly.py full_$MODE < /dev/null &> $log_full &"
	echo "( to find PID use: ps -aux | grep nightly )"
	nohup python -u nightly.py full_$MODE < /dev/null >> $log_full 2>&1 &
	echo "nohup log log_full_$MODE: $log_full"
	echo ""
}

run "ERF"
run "TFR"

