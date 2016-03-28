#! /usr/bin/env python
# coding=utf-8
# Program: Fuzzy slope position extraction based on D-8 and D-infinity algorithms
# 
# Created By:  Liangjun Zhu
# Date From :  3/20/15
# Version   :  5/7/15  v0.1-beta first released version for test.

# Email     :  zlj@lreis.ac.cn
#
import os, sys, time
import TauDEM
from Nomenclature import *
from Config import *
from Util import *
from PreProcessing import PreProcessing
from SelectTypLoc import SelectTypLoc
from FuzzySlpPosInference import FuzzySlpPosInference
from ParasComb import ParametersCombination

if __name__ == '__main__':
    startT = time.time()
    log = ''
    allcost = 0
    ## Stage 1: Preprocessing if needed
    if preprocess:
        PreProcessing(FlowModel)
        endPreprocT = time.time()
        cost = (endPreprocT - startT)
        log = log + "Preprocessing Time-consuming: " + str(cost) + ' s\n'
        allcost = allcost + cost

    ## Stage 2: Selection of Typical Locations and Calculation of Inference Parameters
    if typlocSelection:
        startSelectionT = time.time()
        SelectTypLoc()
        endSelectionT = time.time()
        if preprocess:
            cost = (endSelectionT - endPreprocT)
        else:
            cost = (endSelectionT - startT)
        allcost = allcost + cost
        log = log + "Selection of Typical Locations Time-consuming: " + str(cost) + ' s\n'
    ## Stage 3: Fuzzy Slope Position Inference
    if similarityInference:
        FuzzySlpPosInference()
        endFuzInfT = time.time()
        if typlocSelection:
            cost = (endFuzInfT - endSelectionT)
        elif preprocess:
            cost = (endFuzInfT - endPreprocT)
        else:
            cost = (endFuzInfT - startT)
        log = log + "Fuzzy Slope Position Inference Time-consuming: " + str(cost) + ' s\n'
        allcost = allcost + cost
        log = log + "All mission time-consuming: " + str(allcost) + ' s\n'
    logf = open(Log_runtime, 'a')
    logf.write(log)
    logf.close()
    ## Combine the config files into TypLocExtConf.dat and FuzInfConf.dat
    ParametersCombination(typlocSelection, similarityInference)