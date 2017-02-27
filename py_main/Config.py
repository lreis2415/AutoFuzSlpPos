#! /usr/bin/env python
# coding=utf-8
# @Description: Configuration of preprocessing for AutoFuzSlpPos
# @Author: Liang-Jun Zhu
# @Date:   7/31/15
#

import ConfigParser
from Util import *
from multiprocessing import cpu_count

# Load model configuration from *.ini file
cf = ConfigParser.ConfigParser()
inif, inputProc, rootDir = GetInputArgs()
cf.read(inif)
# 1. Required Inputs
exeDir = None
rawdem = None
if 'REQUIRED' in cf.sections():
    exeDir = cf.get('REQUIRED', 'exeDir'.lower())
    if rootDir is None:
        if cf.has_option('REQUIRED', 'rootDir'.lower()):
            rootDir = cf.get('REQUIRED', 'rootDir'.lower())
        else:
            raise IOError("Workspace must be defined!")
    rawdem = cf.get('REQUIRED', 'rawdem'.lower())
else:
    raise IOError("[REQUIRED] section MUST be existed in *.ini file.")

if not isPathExists(exeDir):
    exeDir = None
if not isPathExists(rootDir):
    os.makedirs(rootDir)
if not isFileExists(rawdem):
    raise ValueError("The DEM file %s is not existed or have no access permission!" % rawdem)

# TODO, currently, the five basic slope position types are supported.
# TODO, 11 slope positions when considering the concavity and convexity along both the contour and profile directions
# TODO, will be considered in the future.
SlpPosItems = ["rdg", "shd", "bks", "fts", "vly"]

# 2. Executable Flags
# Set default flags first.
preprocess = True
typlocSelection = True
similarityInference = True
AutoTypLocExtraction = True
ModifyExtractConfFile = False
AutoInfParams = True
ModifyInfConfFile = False
CalSecHardSlpPos = False
CalSPSI = False
ExtLog = True
# Read from .ini file if stated.
if 'EXECUTABLE_FLAGS' in cf.sections():
    preprocess = cf.getboolean('EXECUTABLE_FLAGS', 'preprocess'.lower())
    typlocSelection = cf.getboolean('EXECUTABLE_FLAGS', 'typlocSelection'.lower())
    similarityInference = cf.getboolean('EXECUTABLE_FLAGS', 'similarityInference'.lower())
    AutoTypLocExtraction = cf.getboolean('EXECUTABLE_FLAGS', 'AutoTypLocExtraction'.lower())
    ModifyExtractConfFile = cf.getboolean('EXECUTABLE_FLAGS', 'ModifyExtractConfFile'.lower())
    AutoInfParams = cf.getboolean('EXECUTABLE_FLAGS', 'AutoInfParams'.lower())
    ModifyInfConfFile = cf.getboolean('EXECUTABLE_FLAGS', 'ModifyInfConfFile'.lower())
    CalSecHardSlpPos = cf.getboolean('EXECUTABLE_FLAGS', 'CalSecHardSlpPos'.lower())
    CalSPSI = cf.getboolean('EXECUTABLE_FLAGS', 'CalSPSI'.lower())
    ExtLog = cf.getboolean('EXECUTABLE_FLAGS', 'ExtLog'.lower())

# 3. Optional Inputs
mpiexeDir = None
hostfile = None
outlet = None
VlySrc = None
RdgSrc = None
rpiFile = None

if 'OPTIONAL' in cf.sections():
    mpiexeDir = cf.get('OPTIONAL', 'mpiexeDir'.lower())
    hostfile = cf.get('OPTIONAL', 'hostfile'.lower())
    outlet = cf.get('OPTIONAL', 'outlet'.lower())
    VlySrc = cf.get('OPTIONAL', 'vlysrc'.lower())
    RdgSrc = cf.get('OPTIONAL', 'rdgsrc'.lower())
    rpiFile = cf.get('OPTIONAL', 'rpiFile'.lower())
    if inputProc <= 0 or inputProc is None:
        if cf.has_option('OPTIONAL', 'inputProc'.lower()):
            inputProc = cf.getint('OPTIONAL', 'inputProc'.lower())
        else:
            inputProc = cpu_count() / 2

if not isPathExists(mpiexeDir):
    mpiexeDir = None
if not isFileExists(hostfile):
    if hostfile.lower() == 'none' or hostfile.lower() == '':
        hostfile = None
    else:
        raise ValueError("The hostfile %s is not existed or have no access permission!" % hostfile)
if not isFileExists(outlet):
    if outlet.lower() == 'none' or outlet.lower() == '':
        outlet = None
    else:
        raise ValueError("The outlet %s is not existed or have no access permission!" % outlet)
if not isFileExists(VlySrc):
    if VlySrc.lower() == 'none' or VlySrc.lower() == '':
        VlySrc = None
    else:
        raise ValueError("The vlysrc %s is not existed or have no access permission!" % VlySrc)

if not isFileExists(RdgSrc):
    if RdgSrc.lower() == 'none' or RdgSrc.lower() == '':
        RdgSrc = None
    else:
        raise ValueError("The RdgSrc %s is not existed or have no access permission!" % RdgSrc)

if not isFileExists(rpiFile):
    if rpiFile.lower() == 'none' or rpiFile.lower() == '':
        rpiFile = None
    else:
        raise ValueError("The rpiFile %s is not existed or have no access permission!" % rpiFile)

# 4. Optional parameters settings for terrain attributes preparation
FlowModel = 1
rpiMethod = 1
SPSImethod = 1
DistanceExponentForIDW = 8
TagDict = dict()
for slppos in SlpPosItems:
    if slppos not in TagDict.keys():
        TagDict[slppos] = 1
maxMoveDist = 50
numthresh = 20
logspace = True
D8StreamThreshold = 0
D8DownMethod = 'Surface'
D8StreamTag = 1
D8UpMethod = 'Surface'
D8UpStats = 'Average'
DinfStreamThreshold = 0
DinfDownStat = 'Average'
DinfDownMethod = 'Surface'
DinfDistDownWG = None
propthresh = 0.0
DinfUpStat = 'Average'
DinfUpMethod = 'Surface'
if 'OPTIONAL_DTA' in cf.sections():
    FlowModel = cf.getint('OPTIONAL_DTA', 'FlowModel'.lower())
    rpiMethod = cf.getint('OPTIONAL_DTA', 'rpiMethod'.lower())
    SPSImethod = cf.getint('OPTIONAL_DTA', 'SPSImethod'.lower())
    DistanceExponentForIDW = cf.getint('OPTIONAL_DTA', 'DistanceExponentForIDW'.lower())
    for slppos in SlpPosItems:
        if cf.has_option('OPTIONAL_DTA', slppos + "tag"):
            TagDict[slppos] = cf.getint('OPTIONAL_DTA', slppos + "tag")
            if TagDict[slppos] <= 0:
                TagDict[slppos] = 1
    maxMoveDist = cf.getfloat('OPTIONAL_DTA', 'maxMoveDist'.lower())
    numthresh = cf.getint('OPTIONAL_DTA', 'numthresh'.lower())
    logspace = cf.getboolean('OPTIONAL_DTA', 'logspace'.lower())
    D8StreamThreshold = cf.getint('OPTIONAL_DTA', 'D8StreamThreshold'.lower())
    D8DownMethod = cf.get('OPTIONAL_DTA', 'D8DownMethod'.lower())
    D8StreamTag = cf.getint('OPTIONAL_DTA', 'D8StreamTag'.lower())
    D8UpMethod = cf.get('OPTIONAL_DTA', 'D8UpMethod'.lower())
    D8UpStats = cf.get('OPTIONAL_DTA', 'D8UpStats'.lower())
    DinfStreamThreshold = cf.getint('OPTIONAL_DTA', 'DinfStreamThreshold'.lower())
    DinfDownStat = cf.get('OPTIONAL_DTA', 'DinfDownStat'.lower())
    DinfDownMethod = cf.get('OPTIONAL_DTA', 'DinfDownMethod'.lower())
    DinfDistDownWG = cf.get('OPTIONAL_DTA', 'DinfDistDownWG'.lower())
    propthresh = cf.getfloat('OPTIONAL_DTA', 'propthresh'.lower())
    DinfUpStat = cf.get('OPTIONAL_DTA', 'DinfUpStat'.lower())
    DinfUpMethod = cf.get('OPTIONAL_DTA', 'DinfUpMethod'.lower())
if FlowModel != 0:
    FlowModel = 1
if rpiMethod != 0:
    rpiMethod = 1
if CalSPSI is True:
    if SPSImethod < 1:
        SPSImethod = 1
    elif SPSImethod > 3:
        SPSImethod = 3
if DistanceExponentForIDW < 0:
    DistanceExponentForIDW = 8
if maxMoveDist < 0:
    maxMoveDist = 50
if numthresh < 0:
    numthresh = 20
if D8StreamThreshold < 0:
    D8StreamThreshold = 0
DistanceMethod = ['Horizontal', 'Vertical', 'Pythagoras', 'Surface']
StatMethod = ['Average', 'Maximum', 'Minimum']
if not StringInList(D8DownMethod, DistanceMethod):
    D8DownMethod = 'Surface'
if D8StreamTag < 0:
    D8StreamTag = 1
if not StringInList(D8UpMethod, DistanceMethod):
    D8UpMethod = 'Surface'
if not StringInList(D8UpStats, StatMethod):
    D8UpStats = 'Average'
if DinfStreamThreshold < 0:
    DinfStreamThreshold = 0
if StringInList(DinfDownStat, StatMethod):
    DinfDownStat = 'Average'
if StringInList(DinfDownMethod, DistanceMethod):
    DinfDownMethod = 'Surface'
if not isFileExists(DinfDistDownWG):
    if DinfDistDownWG.lower() == 'none':
        DinfDistDownWG = None
    else:
        raise ValueError("The DinfDistDownWG %s is not existed or have no access permission!" % hostfile)
if propthresh < 0:
    propthresh = 0.0
if not StringInList(DinfUpStat, StatMethod):
    DinfUpStat = 'Average'
if not StringInList(DinfUpMethod, DistanceMethod):
    DinfUpMethod = 'Surface'

# 5. Optional parameter-settings for Typical Locations selection
RPI_default_path = rootDir + os.sep + 'Params' + os.sep + 'RPI.tif'
ProfC_default_path = rootDir + os.sep + 'Params' + os.sep + 'ProfC.tif'
HorizC_default_path = rootDir + os.sep + 'Params' + os.sep + 'HorizC.tif'
Slope_default_path = rootDir + os.sep + 'Params' + os.sep + 'Slp.tif'
HAND_default_path = rootDir + os.sep + 'Params' + os.sep + 'HAND.tif'
if FlowModel >= 1:
    Elev_default_path = rootDir + os.sep + 'DinfpreDir' + os.sep + 'demfil.tif'
else:
    Elev_default_path = rootDir + os.sep + 'D8preDir' + os.sep + 'demfil.tif'
preDerivedTerrainAttrs = {'rpi'   : RPI_default_path, 'rpifile': rpiFile, 'profc': ProfC_default_path,
                          'horizc': HorizC_default_path, 'slp': Slope_default_path, 'hand': HAND_default_path,
                          'elev'  : Elev_default_path}
regionAttrs = ['rpi', 'rpifile']  # may be extended further
# 5.1 Terrain attributes list
TerrainAttrList = []
TerrainAttrDict = {}
TerrainAttrNum = -1
if cf.has_option('OPTIONAL_TYPLOC', 'TerrainAttrDict'.lower()):
    TerrainAttrDictStr = cf.get('OPTIONAL_TYPLOC', 'TerrainAttrDict'.lower())
    tmpAttrStrs = SplitStr(TerrainAttrDictStr, ',')
    if len(tmpAttrStrs) == 0:
        raise ValueError("You MUST assign terrain attribute directionary (TerrainAttrDict), please check and retry!")
    else:
        TerrainAttrNum = len(tmpAttrStrs)
    if not tmpAttrStrs[0].lower() in regionAttrs:
        raise ValueError("Regional terrain attribute MUST be in the first place!")
    else:
        if isFileExists(tmpAttrStrs[0]):
            TerrainAttrDict['rpi'] = tmpAttrStrs[0]
            TerrainAttrList.append('rpi')
        else:
            TerrainAttrDict['rpi'] = preDerivedTerrainAttrs['rpi']
            TerrainAttrList.append('rpi')
        tmpAttrStrs.remove(tmpAttrStrs[0])
    for tmpStr in tmpAttrStrs:
        if tmpStr.lower() in preDerivedTerrainAttrs.keys():  # predefined terrain attribute
            TerrainAttrDict[tmpStr.lower()] = preDerivedTerrainAttrs[tmpStr.lower()]
            TerrainAttrList.append(tmpStr.lower())
        elif isFileExists(tmpStr):  # user-defined terrain attribute, full file path
            tmpFileName = GetCoreFileName(tmpStr)  # Get core file name (without suffix)
            TerrainAttrDict[tmpFileName.lower()] = tmpStr
            TerrainAttrList.append(tmpFileName.lower())
        else:  # otherwise, throw an exception
            raise ValueError("TerrainAttrDict input is invalid, please follow the instructure!")
else:
    TerrainAttrDict = {'rpi' : RPI_default_path, 'profc': ProfC_default_path, 'slp': Slope_default_path,
                       'hand': HAND_default_path}
    TerrainAttrList = ['rpi', 'profc', 'slp', 'hand']
    TerrainAttrNum = 4
# 5.2 Several basic parameters in selecting typical locations
DefaultBaseParam = [10, 0.1, 0.3, 1, 0.1, 1.414, 50, 4.0]
# BaseParamsName = ['RdgBaseParam', 'ShdBaseParam', 'BksBaseParam', 'FtsBaseParam', 'VlyBaseParam']
AllBaseParams = dict()
for slppos in SlpPosItems:
    name = slppos + "baseparam"
    tmpBaseParam = []
    if cf.has_option('OPTIONAL_TYPLOC', name.lower()):
        BaseParamStr = cf.get('OPTIONAL_TYPLOC', name.lower())
        baseParamFloats = SplitStr4Float(BaseParamStr, ',')
        if len(baseParamFloats) == len(DefaultBaseParam):
            tmpBaseParam = baseParamFloats[:]
        else:
            raise ValueError("Base parameters number for BiGaussian fitting MUST be 8, please check and retry!")
    else:
        tmpBaseParam = DefaultBaseParam[:]
    AllBaseParams[slppos] = tmpBaseParam[:]
# for basepara in AllBaseParams.keys():
#     print basepara, AllBaseParams[basepara]
# 5.4 Pre-defined fuzzy membership function shapes of each terrain attribute for each slope position
# FuzInfNames = ['RdgFuzInfDefault', 'ShdFuzInfDefault', 'BksFuzInfDefault', 'FtsFuzInfDefault', 'VlyFuzInfDefault']
FuzInfDefaults = dict()
for slppos in SlpPosItems:
    name = slppos + "fuzinfdefault"
    if cf.has_option('OPTIONAL_TYPLOC', name.lower()):
        fuzInfShpStr = cf.get('OPTIONAL_TYPLOC', name.lower())
        fuzInfShpStrs = SplitStr(fuzInfShpStr, ',')
        if len(fuzInfShpStrs) != TerrainAttrNum:
            raise ValueError("The number of FMF shape must equal to terrain attribute number!")
        else:
            tmpFuzInfShp = []
            for i in range(TerrainAttrNum):
                tmpFuzInfShp.append([TerrainAttrList[i], fuzInfShpStrs[i]])
            FuzInfDefaults[slppos] = tmpFuzInfShp[:]
    else:  # if no fuzzy inference default parameters
        if TerrainAttrList == ['rpi', 'profc', 'slp', 'hand']:  # only if it is the default terrain attributes list
            if name.lower() == 'rdgfuzinfdefault':
                FuzInfDefaults["rdg"] = [['rpi', 'S'], ['profc', 'S'], ['slp', 'Z'], ['hand', 'SN']]
            elif name.lower() == 'shdfuzinfdefault':
                FuzInfDefaults["shd"] = [['rpi', 'B'], ['profc', 'S'], ['slp', 'B'], ['hand', 'N']]
            elif name.lower() == 'bksfuzinfdefault':
                FuzInfDefaults["bks"] = [['rpi', 'B'], ['profc', 'B'], ['slp', 'S'], ['hand', 'N']]
            elif name.lower() == 'ftsfuzinfdefault':
                FuzInfDefaults["fts"] = [['rpi', 'B'], ['profc', 'ZB'], ['slp', 'ZB'], ['hand', 'N']]
            elif name.lower() == 'vlyfuzinfdefault':
                FuzInfDefaults["vly"] = [['rpi', 'Z'], ['profc', 'B'], ['slp', 'Z'], ['hand', 'N']]
        else:
            raise ValueError("The FuzInfDefault items must be defined corresponding to TerrainAttrDict!")
# for fuzinf in FuzInfDefaults.keys():
#     print fuzinf, FuzInfDefaults[fuzinf]
# 5.5 Value ranges of terrain attributes for extracting prototypes
# ValueRangeNames = ['RdgValueRanges', 'ShdValueRanges', 'BksValueRanges', 'FtsValueRanges', 'VlyValueRanges']
ValueRanges = dict()
if not ModifyExtractConfFile:  # do not read from ExtractConfFile
    for slppos in SlpPosItems:
        name = slppos + "valueranges"
        values = list()
        if cf.has_option('OPTIONAL_TYPLOC', name.lower()):
            rngStr = cf.get('OPTIONAL_TYPLOC', name.lower())
            values = FindNumberFromString(rngStr)
        if values is None and AutoTypLocExtraction:
            if name.lower() == 'rdgvalueranges':
                ValueRanges[slppos] = [[TerrainAttrDict['rpi'], 0.99, 1.0]]
            elif name.lower() == 'shdvalueranges':
                ValueRanges[slppos] = [[TerrainAttrDict['rpi'], 0.9, 0.95]]
            elif name.lower() == 'bksvalueranges':
                ValueRanges[slppos] = [[TerrainAttrDict['rpi'], 0.5, 0.6]]
            elif name.lower() == 'ftsvalueranges':
                ValueRanges[slppos] = [[TerrainAttrDict['rpi'], 0.15, 0.2]]
            elif name.lower() == 'vlyvalueranges':
                ValueRanges[slppos] = [[TerrainAttrDict['rpi'], 0.0, 0.1]]
        elif values is not None or AutoTypLocExtraction:  # value ranges is derived from string
            if len(values) % 3 != 0:
                raise ValueError("%s is unvalid, please follow the instruction and retry!" % name)
            elif len(values) >= 3 and len(values) % 3 == 0:  # one or several value ranges are defined
                tmpRng = list()
                for i in range(len(values) / 3):
                    tmpV = values[i * 3:i * 3 + 3]
                    idx = int(tmpV.pop(0)) - 1
                    if idx < 0 or idx > TerrainAttrNum - 1:
                        raise ValueError("The terrain attribute index must be 1 to %d" % (TerrainAttrNum))
                    tmpV.sort()
                    tmpRng.append([TerrainAttrDict[TerrainAttrList[idx]], tmpV[0], tmpV[1]])
                ValueRanges[slppos] = tmpRng[:]
        else:  # if no value ranges are provided and AutoTypLocExtraction is false
            raise ValueError("%s has no valid numeric values!" % name)
        # complete the value ranges of other terrain attribute
        for rng in ValueRanges.keys():
            rngItem = ValueRanges[rng]
            if len(rngItem) < TerrainAttrNum:
                presentItem = []
                for attr in rngItem:
                    presentItem.append(attr[0])
                for path in TerrainAttrDict.values():
                    if path not in presentItem:
                        rngItem.append([path, 0., 0.])


# for rng in ValueRanges.keys():
#     print rng, ValueRanges[rng]
# 6. Optional parameter-settings for Fuzzy slope position inference
# InferParamNames = ['RdgInferParams', 'ShdInferParams', 'BksInferParams', 'FtsInferParams', 'VlyInferParams']
InferParams = dict()
FMFShape = {1: 'B', 2: 'S', 3: 'Z'}
if not ModifyInfConfFile:
    for slppos in SlpPosItems:
        name = slppos + "inferparams"
        values = list()
        if cf.has_option('OPTIONAL_FUZINF', name.lower()):
            rngStr = cf.get('OPTIONAL_FUZINF', name.lower())
            values = FindNumberFromString(rngStr)
        if values is None and AutoInfParams:
            InferParams[slppos] = []
        elif values is not None and not AutoInfParams:
            if len(values) % 4 == 0 and len(values) / 4 <= TerrainAttrNum:
                tmpInf = list()
                tmpV = list()
                for i in range(len(values) / 4):
                    tmpV = values[i * 4:i * 4 + 4]
                    AttrIdx = int(tmpV.pop(0)) - 1
                    ShpIdx = int(tmpV.pop(0))
                    if AttrIdx < 0 or AttrIdx > len(values) / 4 - 1:
                        raise ValueError("The terrain attribute index must be 1 to %d" % (len(values) / 4))
                    if ShpIdx < 1 or ShpIdx > 3:
                        raise ValueError("The FMF Shape index must be 1, 2, or 3")
                    if FMFShape[ShpIdx] == 'B':  # ['B', 6, 2, 0.5, 6, 2, 0.5]
                        tmpInf.append(['B', tmpV[0], 2, 0.5, tmpV[1], 2, 0.5])
                    elif FMFShape[ShpIdx] == 'S':  # ['S', 6, 2, 0.5, 1, 0, 1]
                        tmpInf.append(['S', tmpV[0], 2, 0.5, 1, 0, 1])
                    elif FMFShape[ShpIdx] == 'Z':  # ['Z', 1, 0, 1, 6, 2, 0.5]
                        tmpInf.append(['Z', 1, 0, 1, tmpV[1], 2, 0.5])
                InferParams[slppos] = tmpInf[:]
            else:
                raise ValueError("%s is unvalid, please follow the instruction and retry!" % name)
        else:
            raise ValueError("%s has no valid numeric values!" % name)
# for infer in InferParams.keys():
#     print infer, InferParams[infer]
