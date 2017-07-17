#! /usr/bin/env python
# coding=utf-8
# @Description: This file contains predefined file names.
# @Author: Liang-Jun Zhu
#
from Config import *
from Util import makeResultFolders

####  Stage 0: Overall setting  ####
PreDir, ParamDir, LogDir, TypLocDir, ConfDir, FSPDir = makeResultFolders(rootDir, FlowModel, preprocess)
####  Stage 1: Preprocessing from DEMsrc  ####
dem = PreDir + os.sep + 'dem.tif'
demfilpre = PreDir + os.sep + 'demfilpre.tif'
demfil = PreDir + os.sep + 'demfil.tif'
log_preproc = LogDir + os.sep + 'log_preprocessing.txt'
Log_all = LogDir + os.sep + 'log_all.txt'
Log_runtime = LogDir + os.sep + 'log_runtime.txt'

# D8 flow model nomenclature
D8FlowDir = PreDir + os.sep + 'D8FlowDir.tif'
D8Slp = PreDir + os.sep + 'D8Slp.tif'
PkrDglStream = PreDir + os.sep + 'PkrDglStream.tif'
outletpre = PreDir + os.sep + 'outlet.shp'
outletM = PreDir + os.sep + 'outletM.shp'
D8ContriArea = PreDir + os.sep + 'D8ContriArea.tif'
drpFile = PreDir + os.sep + 'drpFile.txt'
D8Stream = PreDir + os.sep + 'D8Stream.tif'
D8DistDown = PreDir + os.sep + 'D8DistDown.tif'
D8DistDown_V = PreDir + os.sep + 'D8DistDownElev.tif'
D8DistUp = PreDir + os.sep + 'D8DistUp.tif'
RPID8 = PreDir + os.sep + 'RPID8.tif'
D8StreamOrd = PreDir + os.sep + 'D8Streamord.tif'
NetTree = PreDir + os.sep + 'NetTree.txt'
NetCoord = PreDir + os.sep + 'NetCoord.txt'
D8StreamNet = PreDir + os.sep + 'D8StreamNet.shp'
SubBasin = PreDir + os.sep + 'Subbasins.tif'

# D-infinity flow model nomenclature
DinfFlowDir = PreDir + os.sep + 'DinfFlowDir.tif'
DinfSlp = PreDir + os.sep + 'DinfSlp.tif'
DinfContriArea = PreDir + os.sep + 'DinfContriArea.tif'
DinfStream = PreDir + os.sep + 'DinfStream.tif'
DinfDistDown = PreDir + os.sep + 'DinfDistDown.tif'
DinfDistUp = PreDir + os.sep + 'DinfDistUp.tif'
RPIDinf = PreDir + os.sep + 'RPIDinf.tif'
DinfDistDown_V = PreDir + os.sep + 'DinfDistDownElev.tif'

potRdgFromSubbsn = PreDir + os.sep + 'potrdg.tif'
RdgOrgSrc = PreDir + os.sep + 'rdgorgsrc.tif'
RdgSrcCal = PreDir + os.sep + 'rdgsrc.tif'
VlySrcCal = PreDir + os.sep + 'vlysrc.tif'
dist2Vly = PreDir + os.sep + 'dist2vly.tif'
dist2Rdg = PreDir + os.sep + 'dist2rdg.tif'
RPISkidmore = PreDir + os.sep + 'rpiSkidmore.tif'
# Params files
Slope = ParamDir + os.sep + 'Slp.tif'
HorizC = ParamDir + os.sep + 'HorizC.tif'
ProfC = ParamDir + os.sep + 'ProfC.tif'
RPI = ParamDir + os.sep + 'RPI.tif'
HAND = ParamDir + os.sep + 'HAND.tif'

HANDDict = {'Name': 'HAND', 'Path': HAND, 'Min': 0.0, 'Ave': 0.0, 'Max': 0.0, 'STD': 0.0}
# TerrainRestrict contains Name,Path,MinValue,MaxValue
# for HANDDict, users can change 'Ave', 'Min', 'Max' to numbers.
RdgTerrainRestrict = None  # [[HANDDict,'Name','Path','Ave','Max']]
ShdTerrainRestrict = None  # [[HANDDict,'Name','Path','Ave','Max']]
BksTerrainRestrict = None  # [[HANDDict,'Name','Path',5,'Max']]
FtsTerrainRestrict = None
VlyTerrainRestrict = None  # [[HANDDict,'Name','Path','Min','Ave']]

####   Stage 2: Selection of Typical Locations  ####
DefaultFuzInfLog = ConfDir + os.sep + "DefaultFuzInfLog.dat"
RdgExtConfig = ConfDir + os.sep + "RdgExtConfig.dat"
ShdExtConfig = ConfDir + os.sep + "ShdExtConfig.dat"
BksExtConfig = ConfDir + os.sep + "BksExtConfig.dat"
FtsExtConfig = ConfDir + os.sep + "FtsExtConfig.dat"
VlyExtConfig = ConfDir + os.sep + "VlyExtConfig.dat"
ExtConfigDict = {"rdg": RdgExtConfig, "shd": ShdExtConfig, "bks": BksExtConfig, "fts": FtsExtConfig,
                 "vly": VlyExtConfig}
ExtLogDict = dict()
if ExtLog:
    RdgExtLog = LogDir + os.sep + "RdgExtLog.dat"
    ShdExtLog = LogDir + os.sep + "ShdExtLog.dat"
    BksExtLog = LogDir + os.sep + "BksExtLog.dat"
    FtsExtLog = LogDir + os.sep + "FtsExtLog.dat"
    VlyExtLog = LogDir + os.sep + "VlyExtLog.dat"
    ExtLogDict = {"rdg": RdgExtLog, "shd": ShdExtLog, "bks": BksExtLog, "fts": FtsExtLog, "vly": VlyExtLog}
else:
    ExtLogDict = {"rdg": None, "shd": None, "bks": None, "fts": None, "vly": None}

RdgTyp = TypLocDir + os.sep + "RdgTyp.tif"
ShdTyp = TypLocDir + os.sep + "ShdTyp.tif"
BksTyp = TypLocDir + os.sep + "BksTyp.tif"
FtsTyp = TypLocDir + os.sep + "FtsTyp.tif"
VlyTyp = TypLocDir + os.sep + "VlyTyp.tif"
TypDict = {"rdg": RdgTyp, "shd": ShdTyp, "bks": BksTyp, "fts": FtsTyp, "vly": VlyTyp}
RdgInfRecommend = ConfDir + os.sep + "RdgInfRecommend.dat"
ShdInfRecommend = ConfDir + os.sep + "ShdInfRecommend.dat"
BksInfRecommend = ConfDir + os.sep + "BksInfRecommend.dat"
FtsInfRecommend = ConfDir + os.sep + "FtsInfRecommend.dat"
VlyInfRecommend = ConfDir + os.sep + "VlyInfRecommend.dat"
InfRecommendDict = {"rdg": RdgInfRecommend, "shd": ShdInfRecommend, "bks": BksInfRecommend, "fts": FtsInfRecommend,
                    "vly": VlyInfRecommend}
ExtConfig = ConfDir + os.sep + "ExtConfig.dat"
####   Stage 3: Fuzzy slope position inference  ####

RdgInfConfig = ConfDir + os.sep + "RdgInfConfig.dat"
ShdInfConfig = ConfDir + os.sep + "ShdInfConfig.dat"
BksInfConfig = ConfDir + os.sep + "BksInfConfig.dat"
FtsInfConfig = ConfDir + os.sep + "FtsInfConfig.dat"
VlyInfConfig = ConfDir + os.sep + "VlyInfConfig.dat"
InfConfigDict = {"rdg": RdgInfConfig, "shd": ShdInfConfig, "bks": BksInfConfig, "fts": FtsInfConfig,
                 "vly": VlyInfConfig}
InfConfig = ConfDir + os.sep + "InfConfig.dat"
RdgInf = FSPDir + os.sep + "RdgInf.tif"
ShdInf = FSPDir + os.sep + "ShdInf.tif"
BksInf = FSPDir + os.sep + "BksInf.tif"
FtsInf = FSPDir + os.sep + "FtsInf.tif"
VlyInf = FSPDir + os.sep + "VlyInf.tif"
InfFileDict = {"rdg": RdgInf, "shd": ShdInf, "bks": BksInf, "fts": FtsInf, "vly": VlyInf}
HardenSlpPos = FSPDir + os.sep + "HardenSlpPos.tif"
MaxSimilarity = FSPDir + os.sep + "MaxSimilarity.tif"

SecHardenSlpPos = FSPDir + os.sep + "SecHardenSlpPos.tif"
SecMaxSimilarity = FSPDir + os.sep + "SecMaxSimilarity.tif"

SPSIfile = FSPDir + os.sep + "SPSI.tif"

ProfileFuzSlpPos = FSPDir + os.sep + "ProfileFuzSlpPos.shp"
