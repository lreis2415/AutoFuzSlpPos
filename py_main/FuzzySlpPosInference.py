#! /usr/bin/env python
#coding=utf-8

from Nomenclature import *
from Util import *
import TauDEM
from Config import *
def FuzzySlpPosInference():
    RPIExtInfo = [RdgExtractionInfo[0],ShdExtractionInfo[0],BksExtractionInfo[0],FtsExtractionInfo[0],VlyExtractionInfo[0]]
    tempw1 = RPIExtInfo[0][1] - RPIExtInfo[1][2]
    RdgInferenceInfo.append(['RPI','S',tempw1,2,0.5,1,0,1]) # Ridge:S: w1 = Rdg.min-Shd.max
    tempw = min(RPIExtInfo[1][1]-RPIExtInfo[2][2],RPIExtInfo[0][1]-RPIExtInfo[1][2])
    ShdInferenceInfo.append(['RPI','B',tempw,2,0.5,tempw,2,0.5]) # Shoulder slope:B: w1 = w2 = min(Shd.min-Bks.max, Rdg.min-Shd.max)
    tempw = min(RPIExtInfo[2][1]-RPIExtInfo[3][2],RPIExtInfo[1][1]-RPIExtInfo[2][2])
    BksInferenceInfo.append(['RPI','B',tempw,2,0.5,tempw,2,0.5]) # Back slope:B: w1 = w2 = min(Bks.min-Fts.max, Shd.min-Bks.max)
    tempw = min(RPIExtInfo[3][1]-RPIExtInfo[4][2],RPIExtInfo[2][1]-RPIExtInfo[3][2])
    FtsInferenceInfo.append(['RPI','B',tempw,2,0.5,tempw,2,0.5]) # Foot slope:B: w1 = w2 = min(Fts.min-Vly.max, Bks.min-Fts.max)
    tempw2 = RPIExtInfo[3][1] - RPIExtInfo[4][2]
    VlyInferenceInfo.append(['RPI','Z',1,0,1,tempw2,2,0.5]) # Valley:Z: w2 = Fts.min-Vly.max

    SlpPosItems = [[RdgInfConfig,RdgTyp, RdgTag, RdgInferenceInfo,DistanceExponentForIDW, RdgInf, RdgInfRecommend,RdgExtLog],\
                    [ShdInfConfig,ShdTyp, ShdTag, ShdInferenceInfo,DistanceExponentForIDW, ShdInf, ShdInfRecommend,ShdExtLog],\
                    [BksInfConfig,BksTyp, BksTag, BksInferenceInfo,DistanceExponentForIDW, BksInf,BksInfRecommend,BksExtLog],\
                    [FtsInfConfig,FtsTyp,FtsTag, FtsInferenceInfo,DistanceExponentForIDW, FtsInf,FtsInfRecommend,FtsExtLog],\
                    [VlyInfConfig,VlyTyp, VlyTag, VlyInferenceInfo,DistanceExponentForIDW, VlyInf,VlyInfRecommend,VlyExtLog]]
    

                    
    for SlpPosItem in SlpPosItems:
        if not AutoInfParams:     ## if not use automatically recommended parameters
            if not ModifyInfConfFile:
                configInfo = open(SlpPosItem[0], 'w')
                configInfo.write("PrototypeGRID\t%s\n" % SlpPosItem[1])
                configInfo.write("ProtoTag\t%s\n" % str(SlpPosItem[2]))
                configInfo.write("ParametersNUM\t%s\n" % str(len(SlpPosItem[3])))
                for param in SlpPosItem[3]:
                    configInfo.write("Parameters\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (TerrainAttrDict.get(param[0]),param[1],str(param[2]),str(param[3]),str(param[4]),str(param[5]),str(param[6]),str(param[7])))
                configInfo.write("DistanceExponentForIDW\t%s\n" % str(SlpPosItem[4]))
                configInfo.write("OUTPUT\t%s\n" % SlpPosItem[5])
                configInfo.flush()
                configInfo.close()
        else:
            paramsConfList = []
            for line in open(SlpPosItem[6]):
                paramsConfList.append(line)
            configInfo = open(SlpPosItem[0], 'w')
            configInfo.write("PrototypeGRID\t%s\n" % SlpPosItem[1])
            configInfo.write("ProtoTag\t%s\n" % str(SlpPosItem[2]))
            configInfo.write("ParametersNUM\t%s\n" % str(len(paramsConfList)+1))
            for param in SlpPosItem[3]:
                if param[0] == 'RPI':
                    configInfo.write("Parameters\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (TerrainAttrDict.get(param[0]),param[1],str(param[2]),str(param[3]),str(param[4]),str(param[5]),str(param[6]),str(param[7])))
            for paramline in paramsConfList:
                configInfo.write("%s" % paramline)
            configInfo.write("DistanceExponentForIDW\t%s\n" % str(SlpPosItem[4]))
            configInfo.write("OUTPUT\t%s\n" % SlpPosItem[5])
            configInfo.close()
        TauDEM.FuzzySlpPosInference(SlpPosItem[0],inputProc,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)

    if not CalSecHardSlpPos:
        global SecHardenSlpPos
        SecHardenSlpPos=None
        global SecMaxSimilarity
        SecMaxSimilarity=None
        if not CalSPSI:
            global SPSIfile
            SPSIfile=None
    TauDEM.HardenSlpPos(RdgInf,ShdInf,BksInf,FtsInf,VlyInf,inputProc,HardenSlpPos,MaxSimilarity,sechard=SecHardenSlpPos,secsimi=SecMaxSimilarity,spsim=SPSImethod,spsi=SPSIfile,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
    
