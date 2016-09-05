#! /usr/bin/env python
# coding=utf-8
# @Description: Prepare configuration files for selecting typical location
# @Author: Liang-Jun Zhu
#
import TauDEM
from Nomenclature import *
from Util import *


def SelectTypLoc():
    # ValueRanges contains all predefined value ranges of all terrain attributes
    for slppos in SlpPosItems:
        if not ModifyExtractConfFile:  # Write Extract configuration file only when ModifyExtractConfFile is False
            ExtconfigInfo = open(ExtConfigDict[slppos], 'w')
            ExtconfigInfo.write("ProtoTag\t%s\n" % str(TagDict[slppos]))
            abandon = []  # abandoned terrain attributes (full file path)
            for inf in FuzInfDefaults[slppos]:
                if inf[1] == 'N' or inf[1] == "N":
                    attrName = inf[0]
                    abandon.append(TerrainAttrDict[attrName])
            # print abandon
            paramNum = 0
            for param in ValueRanges[slppos]:
                if param[0] not in abandon:
                    paramNum += 1
            ExtconfigInfo.write("ParametersNUM\t%s\n" % str(paramNum))
            for param in ValueRanges[slppos]:
                for attrName, attrPath in TerrainAttrDict.items():
                    if attrPath == param[0] and param[0] not in abandon:
                        ExtconfigInfo.write("Parameters\t%s\t%s\t%s\t%s\n" % (
                            attrName, attrPath, str(param[1]), str(param[2])))

            ExtconfigInfo.write("OUTPUT\t%s\n" % TypDict[slppos])
            for inf in FuzInfDefaults[slppos]:
                if inf[1] != 'N':
                    ExtconfigInfo.write("FuzInfShp\t%s\t%s\n" % (inf[0], inf[1]))
            baseInputParam = "BaseInput\t"
            for p in AllBaseParams[slppos]:
                baseInputParam = baseInputParam + str(p) + '\t'
            ExtconfigInfo.write(baseInputParam)
            ExtconfigInfo.close()
        TauDEM.SelectTypLocSlpPos(ExtConfigDict[slppos], InfRecommendDict[slppos], inputProc, ExtLogDict[slppos],
                                  mpiexeDir, exeDir, hostfile)
    print "Typical Locations Selected Done!"


if __name__ == '__main__':
    ini, proc, root = GetInputArgs()
    LoadConfiguration(ini, proc, root)
    SelectTypLoc()
