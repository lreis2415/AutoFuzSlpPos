#! /usr/bin/env python
# coding=utf-8

# This file contains all configurations for running the workflow for Fuzzy Slope Postions .
# from Nomenclature import *
import os
import platform

####    Required    ####
## exeDir: if the executable files' path has been exported to the environmental path, set exeDir to None
## rootDir: workspace to store results
## rawdem: input dem, be caution! DEM file should have one cell buffer. If preprocess is False, rawdem could be None.
## outlet: input outlet shapefile, be caution! The outlet point should locate at least one cell inner the DEM boundary.
##         If outlet is None, then the maximum of Contributing Area will be identified as outlet.
##         Also, if preprocess is False, outlet could be None.

sysstr = platform.system()
if sysstr == "Linux":  ## linux cluster
    mpiexeDir = r'/home/zhulj/mpich/bin'
    exeDir = r'/home/zhulj/AutoFuzSlpPos/exec'
    hostfile = r'/home/zhulj/AutoFuzSlpPos/exec/dgpm'
    rootDir = r'/home/zhulj/AutoFuzSlpPos/runtimeTest/1'
    rawdem = r'/home/zhulj/data/PleasantVly/pvDEM_meter_from_3dr.tif'
    outlet = None
    vlysrc = None
    rdgsrc = None
    rpiFile = None  # r'/home/zhulj/AutoFuzSlpPos/basedOriginRPI/Params/RPI.tif'
elif sysstr == "Windows":  ## Windows PC
    mpiexeDir = None
    hostfile = None
    exeDir = r'D:\Compile\AutoFuzSlpPos\Release'
    rootDir = r'E:\data_m\AutoFuzSlpPos\C&G_zhu_2016\AutoResult'
    rawdem = r'E:\data_m\AutoFuzSlpPos\C&G_zhu_2016\rawData\pvDEM_meter_from_3dr.tif'
    outlet = None
    vlysrc = None
    rdgsrc = None  ## if there is ridge or valley source file, assign it here.
    rpiFile = None  ## if rpiFile is assigned, no more RPI will be calculated.
preprocess = True  ## Do preprocess for terrain attributes? True is default.
typlocSelection = True  ## Select typical locations automatically? True is default.
similarityInference = True  ## Calculate fuzzy membership of each slope position? True is default.
inputProc = 1  ## number of processor for parallel computing

####    Optional    ####
FlowModel = 1  ## 0 represents D8 flow model, and 1 represent D-infinity model
rpiMethod = 1  ## Method for Relative Position Index (RPI) calculation, 0 is based on Skidmore's method, and 1 is based on hydrological proximity measures.

AutoTypLocExtraction = True
AutoInfParams = True
ModifyExtractConfFile = True  ## modify typical locations extracting configuration file for another user-defined run
ModifyInfConfFile = True  ## modify the configuration file for another user-defined run

CalSecHardSlpPos = False  ## calculate second harden slope positions or not
CalSPSI = False  ## calculate SPSI (Slope Position Sequence Index) or not, Be Caution, only when CalSecHardSlpPos is True, CalSPSI can be True
SPSImethod = 1  ## only when CalSPSI is True, the SPSImethod would be used. It can be 1,2,3
DistanceExponentForIDW = 8  ## the default is 8
ExtLog = True  ## write logfile

RdgTag = 1
ShdTag = 2
BksTag = 4
FtsTag = 8
VlyTag = 16

###  Optional parameters settings for terrain attributes preparation  ###
maxMoveDist = 50  ## the maximum number of grid cells that the points in the input outlet shapefile will be moved before they are saved to the output outlet shapefile
numthresh = 20  ## the number of steps to divide the search range into when looking for possible threshold values using drop analysis
logspace = 'true'  ## 'true' means use logarithmic spacing for threshold values, 'false' means linear spacing
D8StreamThreshold = 0  ## for D8 stream extraction from DEM, default is 0, which means the value is determined by drop analysis
negD8StreamThreshold = 0  ## for D8 ridge extraction from negative DEM, default is 0, which indicate that the value is equal to D8StreamThreshold
D8DownMethod = 'Surface'  ## for D8DistDownToStream, it can be Horizontal, Vertical, Pythagoras and Surface, the default is 'Surface'
D8StreamTag = 1  ## for D8DistDownToStream, it should be integer, the default is 1
D8UpMethod = 'Surface'  ## for D8DistUpToRidge, it can be Horizontal, Vertical, Pythagoras and Surface, the default is 'Surface'
D8UpStats = 'Average'  ## for D8DistUpToRidge, it can be Average, Maximum, Minimum
DinfStreamThreshold = 0  ## for Dinf stream extraction from DEM, default is 0, which means the value is equal to D8StreamThreshold
negDinfStreamThreshold = 0  ## for Dinf ridge extraction from negative DEM, default is 0, which means the value is equal to DinfStreamThreshold
DinfDownStat = 'Average'  ## used for D-infinity distance down, Average, Maximum, Minimum, and Average is the default
DinfDownMethod = 'Surface'  ## Horizontal, Vertical, Pythagoras, Surface, and Surface is the default
DinfDistDownWG = ''  ## weight grid, the default is ''
propthresh = 0.0  ## proportion threshold parameter where only grid cells that contribute flow with a proportion greater than this user specified threshold (t) is considered to be upslope of any given grid cell
DinfUpStat = 'Average'  ## same as DinfDownStat
DinfUpMethod = 'Surface'  ## same as DinfDownMethod

### Optional parameter-settings for Typical Locations selection  ###
## TerrainAttrDict stores the terrain attributes' name and path.
## 'RPI' is required, or another regional terrain attribute!
RPI_default_path = rootDir + os.sep + 'Params' + os.sep + 'RPI.tif'
ProfC_default_path = rootDir + os.sep + 'Params' + os.sep + 'ProfC.tif'
Slope_default_path = rootDir + os.sep + 'Params' + os.sep + 'Slp.tif'
Elev_default_path = rootDir + os.sep + 'Params' + os.sep + 'HAND.tif'
if rpiFile is None:
    TerrainAttrDict = {'RPI': RPI_default_path, 'ProfC': ProfC_default_path, 'Slope': Slope_default_path,
                       'HAND': Elev_default_path}
else:
    TerrainAttrDict = {'RPI': rpiFile, 'ProfC': ProfC_default_path, 'Slope': Slope_default_path,
                       'HAND': Elev_default_path}

# basic parameters, by default: MIN_FREQUENCY = 10, MIN_TYPLOC_NUM_PECENT = 0.01,\
#          MAX_TYPLOC_NUM_PERCENT = 0.2, SELECTION_MODE = 1,\
#          DEFAULT_INCREMENT_RATIO = 0.1, DEFAULT_SIGMA_MULTIPLIER = 1.414,\
#          MAX_LOOP_NUM_TYPLOC_SELECTION = 50, DEFAULT_BiGaussian_Ratio = 4.0
RdgBaseParam = [10, 0.1, 0.3, 1, 0.1, 1.414, 50, 4.0]
ShdBaseParam = [10, 0.1, 0.3, 1, 0.1, 1.414, 50, 4.0]
BksBaseParam = [10, 0.1, 0.3, 1, 0.1, 1.414, 50, 4.0]
FtsBaseParam = [10, 0.1, 0.3, 1, 0.1, 1.414, 50, 4.0]
VlyBaseParam = [10, 0.1, 0.3, 1, 0.1, 1.414, 50, 4.0]
## Predefined Fuzzy Membership Function Shape, Bell-shaped, S-shaped, Z-shaped and N means Not used.
## These parameters are user-defined.
RdgFuzInfDefault = [['RPI', 'S'], ['ProfC', 'S'], ['Slope', 'Z'], ['HAND', 'SN']]
ShdFuzInfDefault = [['RPI', 'B'], ['ProfC', 'S'], ['Slope', 'B'], ['HAND', 'N']]
BksFuzInfDefault = [['RPI', 'B'], ['ProfC', 'B'], ['Slope', 'S'], ['HAND', 'N']]
FtsFuzInfDefault = [['RPI', 'B'], ['ProfC', 'ZB'], ['Slope', 'ZB'], ['HAND', 'N']]
VlyFuzInfDefault = [['RPI', 'Z'], ['ProfC', 'B'], ['Slope', 'Z'], ['HAND', 'N']]

## default RPI value range for Ridge, Shoulder slope, Backslope, Footslope and valley.
## These parameters are user-defined.
if AutoTypLocExtraction:
    RdgExtractionInfo = [['RPI', 0.99, 1.0]]
    ShdExtractionInfo = [['RPI', 0.9, 0.95]]
    BksExtractionInfo = [['RPI', 0.5, 0.6]]
    FtsExtractionInfo = [['RPI', 0.15, 0.2]]
    VlyExtractionInfo = [['RPI', 0.0, 0.1]]
else:
    RdgExtractionInfo = [['RPI', 0.99, 1.0], ['ProfC', 0.00, 1.0], ['Slope', 0.0, 1.0]]
    ShdExtractionInfo = [['RPI', 0.9, 0.95], ['ProfC', 0.005, 1.0]]
    BksExtractionInfo = [['RPI', 0.5, 0.6], ['ProfC', -0.0001, 0.0001], ['Slope', 10.0, 90.0]]
    FtsExtractionInfo = [['RPI', 0.15, 0.2], ['ProfC', -1.0, -0.005]]
    VlyExtractionInfo = [['RPI', 0.0, 0.1], ['ProfC', -0.0001, 0.0001], ['Slope', 0.0, 1.0]]

### Optional parameter-settings for Fuzzy slope position inference  ###

# Default	w1	r1	k1	w2	r2	k2
# B         6	2	0.5	6	2	0.5
# S         6	2	0.5	1	0	1
# Z         1	0	1	6	2	0.5
InfFuncParam = [['B', 6, 2, 0.5, 6, 2, 0.5], ['S', 6, 2, 0.5, 1, 0, 1], ['Z', 1, 0, 1, 6, 2, 0.5]]
if AutoInfParams:
    RdgInferenceInfo = []
    ShdInferenceInfo = []
    BksInferenceInfo = []
    FtsInferenceInfo = []
    VlyInferenceInfo = []
else:  ## Users can edit either the InferenceInfo below or the InfConfig.dat in Config folder.
    RdgInferenceInfo = [['RPI', 'S', 0.1, 2, 0.5, 1, 0, 1], ['ProfC', 'S', 0.005, 2, 0.5, 1, 0, 1],
                        ['Slope', 'Z', 1, 0, 1, 5, 2, 0.5], ['HAND', 'S', 5, 2, 0.5, 1, 0, 1]]
    ShdInferenceInfo = [['RPI', 'B', 0.05, 2, 0.5, 0.05, 2, 0.5], ['ProfC', 'S', 0.005, 2, 0.5, 1, 0, 1],
                        ['Slope', 'B', 5, 2, 0.5, 5, 2, 0.5]]
    BksInferenceInfo = [['RPI', 'B', 0.3, 2, 0.5, 0.3, 2, 0.5], ['ProfC', 'B', 0.005, 2, 0.5, 0.005, 2, 0.5],
                        ['Slope', 'S', 5, 2, 0.5, 1, 0, 1]]
    FtsInferenceInfo = [['RPI', 'B', 0.05, 2, 0.5, 0.05, 2, 0.5], ['ProfC', 'Z', 1, 0, 1, 0.005, 2, 0.5],
                        ['Slope', 'B', 5, 2, 0.5, 5, 2, 0.5]]
    VlyInferenceInfo = [['RPI', 'Z', 1, 0, 1, 0.1, 2, 0.5], ['ProfC', 'B', 0.005, 2, 0.5, 0.005, 2, 0.5],
                        ['Slope', 'Z', 1, 0, 1, 5, 2, 0.5]]
