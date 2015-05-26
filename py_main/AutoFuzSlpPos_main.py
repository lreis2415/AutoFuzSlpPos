#! /usr/bin/env python
#coding=utf-8
# Program: Fuzzy slope position extraction based on D-8 and D-infinity algorithms
# 
# Created By:  Liangjun Zhu
# Date From :  3/20/15
# Version   :  5/7/15  v0.1-beta first released version for test.
               
# Email     :  zlj@lreis.ac.cn
#
import os,sys,time
import TauDEM
from Nomenclature import *
from Config import *
from Util import *
from PreProcessing import PreProcessing
from SelectTypLoc import SelectTypLoc
from FuzzySlpPosInference import FuzzySlpPosInference

if __name__ == '__main__':
    startT = time.time()
    log = ''
    ## Stage 1: Preprocessing if needed
    if preprocess:
        log = log + "Preprocessing Time-consuming: "
        PreProcessing(FlowModel)
        endPreprocT = time.time()
        cost = (endPreprocT - startT)
        log = log + str(cost) + ' s\n'
    startSelectionT = time.time()
    ## Stage 2: Selection of Typical Locations and Calculation of Inference Parameters
    log = log + "Selection of Typical Locations Time-consuming: "
    SelectTypLoc()
    endSelectionT = time.time()
    if preprocess:
        cost = (endSelectionT - endPreprocT)
    else:
        cost = (endSelectionT - startT)
    log = log + str(cost) + ' s\n'
    ## Stage 3: Fuzzy Slope Position Inference
    log = log + "Fuzzy Slope Position Inference Time-consuming: "
    FuzzySlpPosInference()
    endFuzInfT = time.time()
    cost = (endFuzInfT - endSelectionT )
    log = log + str(cost) + ' s\n'
    
    logf = open(Log_runtime, 'a')
    logf.write(log)
    logf.close()
