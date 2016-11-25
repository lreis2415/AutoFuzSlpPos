#!/bin/bash
# Run AutoFuzSlpPos on 1, 2, 4, 8, 16, 32 processes
scriptpath=/home/zhulj/AutoFuzSlpPos/py_main/main.py
inipath=/home/zhulj/AutoFuzSlpPos/data/pv_dgpm.ini
rootdir=/home/zhulj/AutoFuzSlpPos/runtimeTest
for proc in 1 2 4 8 16 32
	do
		echo "current process number is: $proc "
		python $scriptpath -ini $inipath -proc $proc -root $rootdir/$proc
	done