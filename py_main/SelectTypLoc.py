#! /usr/bin/env python
#coding=utf-8

from Nomenclature import *
from Util import *
import TauDEM
from Config import *
import types
def SelectTypLoc():
    if AutoTypLocExtraction:
        for param in TerrainAttrDict.iterkeys():
            if param != 'RPI':
                RdgExtractionInfo.append([param,0.0,0.0])                                                            
                ShdExtractionInfo.append([param,0.0,0.0])
                BksExtractionInfo.append([param,0.0,0.0])
                FtsExtractionInfo.append([param,0.0,0.0])
                VlyExtractionInfo.append([param,0.0,0.0])
   
    TypLocItems = [["rdg",RdgExtConfig,RdgTyp, RdgTag,RdgExtractionInfo,DistanceExponentForIDW, RdgInf,RdgInfRecommend, RdgExtLog,RdgFuzInfDefault,RdgTerrainRestrict],\
                    ["shd",ShdExtConfig,ShdTyp, ShdTag,ShdExtractionInfo,DistanceExponentForIDW, ShdInf,ShdInfRecommend, ShdExtLog,ShdFuzInfDefault,ShdTerrainRestrict],\
                    ["bks",BksExtConfig,BksTyp, BksTag,BksExtractionInfo,DistanceExponentForIDW, BksInf,BksInfRecommend, BksExtLog,BksFuzInfDefault,BksTerrainRestrict],\
                    ["fts",FtsExtConfig,FtsTyp, FtsTag,FtsExtractionInfo,DistanceExponentForIDW, FtsInf,FtsInfRecommend, FtsExtLog,FtsFuzInfDefault,FtsTerrainRestrict],\
                    ["vly",VlyExtConfig,VlyTyp, VlyTag,VlyExtractionInfo,DistanceExponentForIDW, VlyInf,VlyInfRecommend, VlyExtLog,VlyFuzInfDefault,VlyTerrainRestrict]]

    for item in TypLocItems:
        if AutoTypLocExtraction or not ModifyExtractConfFile:
            ExtconfigInfo = open(item[1], 'w')
            ExtconfigInfo.write("ProtoTag\t%s\n" % str(item[3]))
            ExtconfigInfo.write("ParametersNUM\t%s\n" % str(len(item[4])))
            for param in item[4]:
                ExtconfigInfo.write("Parameters\t%s\t%s\t%s\t%s\n" % (param[0],TerrainAttrDict.get(param[0]),str(param[1]),str(param[2])))
            if item[10] is not None:
                ExtconfigInfo.write("AdditionalNUM\t%s\n" % str(len(item[10])))
                for addparam in item[10]:
                    if type(addparam[0]) is types.DictionaryType:
                        if addparam[0]['Name'] == 'HAND':
                            HANDDict['Min'],HANDDict['Max'],HANDDict['Ave'],HANDDict['STD'] = RasterStatistics(HAND)
                        ExtconfigInfo.write("Additional\t%s\t%s\t%s\t%s\n" % (addparam[0][addparam[1]],addparam[0][addparam[2]],addparam[0][addparam[3]],addparam[0][addparam[4]]))
                    else:
                        ExtconfigInfo.write("Additional\t%s\t%s\t%s\t%s\n" % (addparam[0],addparam[1],addparam[2],addparam[3]))
            ExtconfigInfo.write("OUTPUT\t%s\n" % item[2])
            for i in range(len(item[9])):
                ExtconfigInfo.write("FuzInfShp\t%s\t%s\n" % (item[9][i][0],item[9][i][1]))
            ExtconfigInfo.close()
        TauDEM.SelectTypLocSlpPos(item[1],item[7],inputProc,item[8],mpiexeDir=mpiexeDir,exeDir)
    print "Typical Locations Selected Done!"