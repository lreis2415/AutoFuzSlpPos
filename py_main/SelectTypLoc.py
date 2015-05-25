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
   
    TypLocItems = [["rdg",RdgExtConfig,RdgTyp, RdgTag,RdgExtractionInfo,DistanceExponentForIDW, RdgInf,RdgInfRecommend, RdgExtLog,RdgFuzInfDefault,RdgTerrainRestrict,RdgBaseParam],\
                    ["shd",ShdExtConfig,ShdTyp, ShdTag,ShdExtractionInfo,DistanceExponentForIDW, ShdInf,ShdInfRecommend, ShdExtLog,ShdFuzInfDefault,ShdTerrainRestrict,ShdBaseParam],\
                    ["bks",BksExtConfig,BksTyp, BksTag,BksExtractionInfo,DistanceExponentForIDW, BksInf,BksInfRecommend, BksExtLog,BksFuzInfDefault,BksTerrainRestrict,BksBaseParam],\
                    ["fts",FtsExtConfig,FtsTyp, FtsTag,FtsExtractionInfo,DistanceExponentForIDW, FtsInf,FtsInfRecommend, FtsExtLog,FtsFuzInfDefault,FtsTerrainRestrict,FtsBaseParam],\
                    ["vly",VlyExtConfig,VlyTyp, VlyTag,VlyExtractionInfo,DistanceExponentForIDW, VlyInf,VlyInfRecommend, VlyExtLog,VlyFuzInfDefault,VlyTerrainRestrict,VlyBaseParam]]

    for item in TypLocItems:
        if AutoTypLocExtraction or not ModifyExtractConfFile:
            ExtconfigInfo = open(item[1], 'w')
            ExtconfigInfo.write("ProtoTag\t%s\n" % str(item[3]))
            abandon = ''
            for i in range(len(item[9])):
                if item[9][i][1] == 'N':
                    abandon = abandon + item[9][i][0]
            #print abandon
            paramNum = 0
            for param in item[4]:
                if abandon.find(param[0]) < 0:
                    paramNum = paramNum + 1
            ExtconfigInfo.write("ParametersNUM\t%s\n" % str(paramNum))
            for param in item[4]:
                if abandon.find(param[0]) < 0:
                    ExtconfigInfo.write("Parameters\t%s\t%s\t%s\t%s\n" % (param[0],TerrainAttrDict.get(param[0]),str(param[1]),str(param[2])))
            if item[10] is not None:
                ExtconfigInfo.write("AdditionalNUM\t%s\n" % str(len(item[10])))
                for addparam in item[10]:
                    if type(addparam[0]) is types.DictionaryType:
                        if addparam[0]['Name'] == 'HAND':
                            HANDDict['Min'],HANDDict['Max'],HANDDict['Ave'],HANDDict['STD'] = RasterStatistics(HAND)
                            if addparam[3] == 'Min' or addparam[3] == 'Max' or addparam[3] == 'Ave':
                                addparam[3] = addparam[0][addparam[3]]
                            if addparam[4] == 'Min' or addparam[4] == 'Max' or addparam[4] == 'Ave':
                                addparam[4] = addparam[0][addparam[4]]
                        ExtconfigInfo.write("Additional\t%s\t%s\t%s\t%s\n" % (addparam[0][addparam[1]],addparam[0][addparam[2]],addparam[3],addparam[4]))
                    else:
                        ExtconfigInfo.write("Additional\t%s\t%s\t%s\t%s\n" % (addparam[0],addparam[1],addparam[2],addparam[3]))
            ExtconfigInfo.write("OUTPUT\t%s\n" % item[2])
            for inf in item[9]:
                if inf[1] != 'N':
                    ExtconfigInfo.write("FuzInfShp\t%s\t%s\n" % (inf[0],inf[1]))
            baseInputParam = "BaseInput\t"
            for p in item[11]:
                baseInputParam = baseInputParam + str(p) + '\t'
            ExtconfigInfo.write(baseInputParam)
            ExtconfigInfo.close()
        #TauDEM.SelectTypLocSlpPos(item[1],item[7],inputProc,item[8],mpiexeDir=mpiexeDir,exeDir=exeDir)
    print "Typical Locations Selected Done!"