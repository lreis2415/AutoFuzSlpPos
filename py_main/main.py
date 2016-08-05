#! /usr/bin/env python
# coding=utf-8
# @Description: Fuzzy slope position extraction based on D-8 and D-infinity algorithms
# 
# @Author:  Liang-Jun Zhu
# @Date  :  3/20/15
# @Email :  zlj@lreis.ac.cn
#
import time
from FuzzySlpPosInference import FuzzySlpPosInference
from Nomenclature import *
from ParasComb import ParametersCombination
from PreProcessing import PreProcessing
from SelectTypLoc import SelectTypLoc

if __name__ == '__main__':
    startT = time.time()
    ini, proc, root = GetInputArgs()
    LoadConfiguration(ini, proc, root)
    log = ''
    allcost = 0
    # Stage 1: Preprocessing if needed
    if preprocess:
        PreProcessing(FlowModel)
        endPreprocT = time.time()
        cost = (endPreprocT - startT)
        log = log + "Preprocessing Time-consuming: " + str(cost) + ' s\n'
        allcost = allcost + cost
    else:
        endPreprocT = time.time()
    # Stage 2: Selection of Typical Locations and Calculation of Inference Parameters
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
    else:
        endSelectionT = time.time()
    # Stage 3: Fuzzy Slope Position Inference
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
    # Combine the config files into TypLocExtConf.dat and FuzInfConf.dat
    ParametersCombination(typlocSelection, similarityInference)
