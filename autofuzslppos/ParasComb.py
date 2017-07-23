#! /usr/bin/env python
# coding=utf-8
# @Description: Combine parameter results for text files for further analysis.
# @Author: Liang-Jun Zhu
#
from Nomenclature import *


def readExtConf(extFile):
    f = open(extFile)
    lines = f.readlines()
    f.close()
    extConfData = []
    # Read the number of records
    recNum = int(lines[1].split('\n')[0].split('\t')[1])
    extConfData.append(recNum)
    for i in range(0, recNum):
        tempConf = lines[i + 2].split('\n')[0].split('\t')
        if StringMatch(tempConf[1], 'profc'):
            minV = 1000. * float(tempConf[3])
            maxV = 1000. * float(tempConf[4])
        else:
            minV = float(tempConf[3])
            maxV = float(tempConf[4])
        minS = str(round(minV, 2))
        maxS = str(round(maxV, 2))
        extConfData.append([tempConf[1], minS, maxS])
    return extConfData


def ExtConfParasComb():
    extConfLines = []
    extConfLines.append([' '])
    for slppos in SlpPosItems:
        tempExtData = readExtConf(ExtConfigDict[slppos])
        tempExtConfLine = [slppos]
        for i in range(tempExtData[0]):
            tempExtConfLine.append(' ')
        for i in range(tempExtData[0]):
            if tempExtData[i + 1][0] not in extConfLines[0]:
                extConfLines[0].append(tempExtData[i + 1][0])
            idx = extConfLines[0].index(tempExtData[i + 1][0])
            if idx >= len(tempExtConfLine):
                for j in range(idx - len(tempExtConfLine) + 1):
                    tempExtConfLine.append(' ')
            tempExtConfLine[idx] = "[" + tempExtData[i + 1][1] + ", " + tempExtData[i + 1][2] + "]"
        extConfLines.append(tempExtConfLine)
    # print extConfLines
    ## Write to ExtConfig
    f = open(ExtConfig, 'w')
    for line in extConfLines:
        for elem in line:
            f.write("%s\t" % elem)
        f.write("\n")
    f.close()


def readInfConf(extFile):
    f = open(extFile)
    lines = f.readlines()
    f.close()
    InfConfData = []
    # Read the number of records
    recNum = int(lines[2].split('\n')[0].split('\t')[1])
    InfConfData.append(recNum)
    for i in range(0, recNum):
        tempConf = lines[i + 3].split('\n')[0].split('\t')
        ## tempConf[3] is Curve shape, tempConf[4] and tempConf[7] is w1 and w2
        if StringMatch(tempConf[1], 'profc'):
            w1V = 1000. * float(tempConf[4])
            w2V = 1000. * float(tempConf[7])
        else:
            w1V = float(tempConf[4])
            w2V = float(tempConf[7])
        w1S = str(round(w1V, 2))
        w2S = str(round(w2V, 2))
        InfConfData.append([tempConf[1], tempConf[3], w1S, w2S])
    return InfConfData


def InfConfParasComb():
    infConfLines = []
    infConfLines.append([' '])
    for slppos in SlpPosItems:
        tempInfData = readInfConf(InfConfigDict[slppos])
        tempInfConfLine = [slppos]
        for i in range(tempInfData[0]):
            tempInfConfLine.append(' ')
        for i in range(tempInfData[0]):
            if tempInfData[i + 1][0] not in infConfLines[0]:
                infConfLines[0].append(tempInfData[i + 1][0])
            idx = infConfLines[0].index(tempInfData[i + 1][0])
            if idx >= len(tempInfConfLine):
                for j in range(idx - len(tempInfConfLine) + 1):
                    tempInfConfLine.append(' ')
            if tempInfData[i + 1][1] == 'B':
                if tempInfData[i + 1][2] == tempInfData[i + 1][3]:
                    tempInfConfLine[idx] = tempInfData[i + 1][1] + ": w1 = w2 = " + tempInfData[i + 1][2]
                else:
                    tempInfConfLine[idx] = tempInfData[i + 1][1] + ": w1 = " + tempInfData[i + 1][2] + ", w2 = " + \
                                           tempInfData[i + 1][3]
            elif tempInfData[i + 1][1] == 'S':
                tempInfConfLine[idx] = tempInfData[i + 1][1] + ": w1 = " + tempInfData[i + 1][2]
            else:
                tempInfConfLine[idx] = tempInfData[i + 1][1] + ": w2 = " + tempInfData[i + 1][3]
        infConfLines.append(tempInfConfLine)
    # print infConfLines
    ## Write to ExtConfig
    f = open(InfConfig, 'w')
    for line in infConfLines:
        for elem in line:
            f.write("%s\t" % elem)
        f.write("\n")
    f.close()


def ParametersCombination(typlocSelection = True, similarityInference = True):
    if typlocSelection:
        ExtConfParasComb()
    if similarityInference:
        InfConfParasComb()


if __name__ == '__main__':
    ini, proc, root = get_input_args()
    LoadConfiguration(ini, proc, root)
    ParametersCombination()
