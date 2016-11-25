#!/bin/bash
# Run AutoFuzSlpPos on different DEFAULT_BiGaussian_Ratio, i.e., 2,3,5,6
for para in 2 3 5 6
	do
		echo "current paraess number is: $para "
		python /home/zhulj/AutoFuzSlpPos/Para.Sensitive/Threshold/py_mainP$para/main.py
	done