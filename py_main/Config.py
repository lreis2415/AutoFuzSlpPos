#! /usr/bin/env python
#coding=utf-8

# This file contains all configuration for running the Fuzzy Slope Postion workflow.
# from Nomenclature import *
import os,platform
## Stage 0: Configuration 
    
####    Required    ####
## exeDir: if the executable files' path has been exported to the environmental path, set exeDir to None
## rootDir: workspace to store results
## rawdem: input dem, be caution! DEM file should have one cell buffer. If preprocess is False, rawdem could be None.
## outlet: input outlet shapefile, be caution! The outlet point should locate at least one cell inner the DEM boundary.
##         If outlet is None, then the maximum of Contributing Area will be identified as outlet.
##         Also, if preprocess is False, outlet could be None.

sysstr = platform.system()
if sysstr == "Linux":
    ## linux cluster
    mpiexeDir = r'/home/zhulj/mpich/bin'
    exeDir = r'/home/zhulj/AutoFuzSlpPos/exec_linux_x86'
    hostfile = r'/home/zhulj/AutoFuzSlpPos/exec_linux_x86/dgpm'
    rootDir = r'/home/zhulj/PV_Dinf/1'
    rawdem = r'/home/zhulj/AutoFuzSlpPos/data/PleasantValley/pvdem.tif'
    outlet = None
    vlysrc = None
    rdgsrc = None
elif sysstr == "Windows":
    ## windows 7
    mpiexeDir = None 
    exeDir = r'E:\github-zlj\AutoFuzSlpPos\exec_win_x86'
    hostfile = None
    rootDir = r'C:\AutoFuzSlpPos\data\PV_Dinf'
    rawdem = r'C:\AutoFuzSlpPos\data\PleasantValley\pvdem.tif'
    outlet = None
    vlysrc = None
    rdgsrc = None                                        ## if there is ridge or valley source file, assign it here.  
                              
preprocess = True                                        ## if preprocessing for parameters' grids is needed, and True by default.
inputProc = 1                                           ## parallel processor's number
FlowModel = 1                                            ## 0 represents D8 flow model, and 1 represent D-infinity model                  

## Selection of Typical Locations
                                                         ## TerrainAttrDict stores the terrain attributes' name and grid path. 'RPI' is required!
                                                         ## By default: TerrainAttrDict = {'RPI':RPI,'ProfC':ProfC_mask,'HorizC':HorizC_mask,'Slope':Slope}

TerrainAttrDict = {'RPI':rootDir + os.sep + 'Params'+ os.sep + 'RPI.tif',\
                   'ProfC':rootDir + os.sep + 'Params'+ os.sep + 'ProfC.tif',\
                   'Slope':rootDir + os.sep + 'Params'+ os.sep + 'Slp.tif',\
                   'HAND':rootDir + os.sep + 'Params'+ os.sep + 'HAND.tif'}

                                                         ## Predefined Fuzzy Membership Function Shape, Bell-shaped, S-shaped, Z-shaped and N means Not used.
RdgFuzInfDefault = [['RPI','S'],['ProfC','S'],['Slope','Z'],['HAND','S']]
ShdFuzInfDefault = [['RPI','B'],['ProfC','S'],['Slope','B'],['HAND','N']]
BksFuzInfDefault = [['RPI','B'],['ProfC','B'],['Slope','S'],['HAND','N']]
FtsFuzInfDefault = [['RPI','B'],['ProfC','ZB'],['Slope','Z'],['HAND','N']]
VlyFuzInfDefault = [['RPI','Z'],['ProfC','B'],['Slope','Z'],['HAND','Z']]
AutoTypLocExtraction = True
ModifyExtractConfFile = True                                ## if user modified the configuration file
AutoInfParams = True
ModifyInfConfFile = True                                     ## modify the configuration file

if AutoTypLocExtraction:
    RdgExtractionInfo = [['RPI',0.95,1.0]]               ## default RPI value range for Ridge, Shoulder, Back, Foot and valley.                                              
    ShdExtractionInfo = [['RPI',0.8,0.9]]
    BksExtractionInfo = [['RPI',0.5,0.6]]
    FtsExtractionInfo = [['RPI',0.2,0.3]]
    VlyExtractionInfo = [['RPI',0.0,0.1]]

####    Optional    ####

deltaElev = 0.01
maxMoveDist = 50                                         ## the maximum number of grid cells that the points in the input outlet shapefile will be moved before they are saved to the output outlet shapefile
numthresh = 20                                           ## the number of steps to divide the search range into when looking for possible threshold values using drop analysis
logspace = 'true'                                        ## 'true' means use logarithmic spacing for threshold values, 'false' means linear spacing

D8StreamThreshold = 0                                    ## for D8 stream extraction from DEM, default is 0, which means the value is determined by drop analysis
negD8StreamThreshold = 0                                 ## for D8 ridge extraction from negative DEM, default is 0, which indicate that the value is equal to D8StreamThreshold

D8DownMethod = 'Surface'                                 ## for D8DistDownToStream, it can be Horizontal, Vertical, Pythagoras and Surface, the default is 'Surface'
D8StreamTag = 1                                          ## for D8DistDownToStream, it should be integer, the default is 1
D8UpMethod =  'Surface'                                  ## for D8DistUpToRidge, it can be Horizontal, Vertical, Pythagoras and Surface, the default is 'Surface'
D8UpStats = 'Average'                                    ## for D8DistUpToRidge, it can be Average, Maximum, Minimum

DinfStreamThreshold = 0                                  ## for Dinf stream extraction from DEM, default is 0, which means the value is equal to D8StreamThreshold
negDinfStreamThreshold = 0                               ## for Dinf ridge extraction from negative DEM, default is 0, which means the value is equal to DinfStreamThreshold

DinfDownStat = 'Average'                                 ## used for D-infinity distance down, Average, Maximum, Minimum, and Average is the default
DinfDownMethod = 'Surface'                               ## Horizontal, Vertical, Pythagoras, Surface, and Surface is the default
DinfDistDownWG = ''                                      ## weight grid, the default is none
propthresh = 0.0                                         ## The proportion threshold parameter where only grid cells that contribute flow with a proportion greater than this user specified threshold (t) is considered to be upslope of any given grid cell
DinfUpStat = 'Average'                                   ## same as DinfDownStat
DinfUpMethod = 'Surface'                                 ## same as DinfDownMethod

## Selection of Typical Locations

# basic parameters
 
# Default: MIN_FREQUENCY = 1, MIN_TYPLOC_NUM = 200,\
#          MAX_TYPLOC_NUM = 2000, DEFAULT_SELECT_RATIO = 0.1,\
#          DEFAULT_INCREMENT_RATIO = 0.1, DEFAULT_SIGMA_MULTIPLIER = 1.414,\
#          MAX_LOOP_NUM_TYPLOC_SELECTION = 100
RdgBaseParam = [1,200,2000,0.1,0.1,1.414,100]
ShdBaseParam = [1,200,2000,0.1,0.1,1.414,100]
BksBaseParam = [1,200,2000,0.1,0.1,1.414,100]
FtsBaseParam = [1,200,2000,0.1,0.1,1.414,100]
VlyBaseParam = [1,200,2000,0.1,0.1,1.414,100]

RdgTag = 1
ShdTag = 2
BksTag = 4
FtsTag = 8
VlyTag = 16

ExtLog = True                                            

if not AutoTypLocExtraction:
    RdgExtractionInfo = [['RPI',0.99,1.0],['ProfC',0.00,1.0],['Slope',0.0,1.0]]                                                    
    ShdExtractionInfo = [['RPI',0.9,0.95],['ProfC',0.005,1.0]]
    BksExtractionInfo = [['RPI',0.5,0.6],['ProfC',-0.0001,0.0001],['Slope',10.0,90.0]]
    FtsExtractionInfo = [['RPI',0.15,0.2],['ProfC',-1.0,-0.005]]
    VlyExtractionInfo = [['RPI',0.0,0.1],['ProfC',-0.0001,0.0001],['Slope',0.0,1.0]]
   

    
## Fuzzy slope position inference
#UnifiedFuzInfParam = True                                ## use unified fuzzy inference parameters for every typical locations or not
                                                         ## when AutoInfParams is Ture, the program will generate inference parameters automatically.
                                                         ## if AutoInfParams is False, it means users can edit either the InferenceInfo below or the InfConfig.dat in Config Folder. 
# Default	w1	r1	k1	w2	r2	k2
# B         6	2	0.5	6	2	0.5
# S         6	2	0.5	1	0	1
# Z         1	0	1	6	2	0.5
InfFuncParam = [['B',6,2,0.5,6,2,0.5],['S',6,2,0.5,1,0,1],['Z',1,0,1,6,2,0.5]]
if not AutoInfParams:
    RdgInferenceInfo = [['RPI','S',0.1,2,0.5,1,0,1],['ProfC','S',0.005,2,0.5,1,0,1],['Slope','Z',1,0,1,5,2,0.5]]
    ShdInferenceInfo = [['RPI','B',0.05,2,0.5,0.05,2,0.5],['ProfC','S',0.005,2,0.5,1,0,1],['Slope','B',5,2,0.5,5,2,0.5]]
    BksInferenceInfo = [['RPI','B',0.3,2,0.5,0.3,2,0.5],['ProfC','B',0.005,2,0.5,0.005,2,0.5],['Slope','S',5,2,0.5,1,0,1]]
    FtsInferenceInfo = [['RPI','B',0.05,2,0.5,0.05,2,0.5],['ProfC','Z',1,0,1,0.005,2,0.5],['Slope','B',5,2,0.5,5,2,0.5]]
    VlyInferenceInfo = [['RPI','Z',1,0,1,0.1,2,0.5],['ProfC','B',0.005,2,0.5,0.005,2,0.5],['Slope','Z',1,0,1,5,2,0.5]]
else:
    RdgInferenceInfo = []
    ShdInferenceInfo = []
    BksInferenceInfo = []
    FtsInferenceInfo = []
    VlyInferenceInfo = []
    

CalSecHardSlpPos = False                                ## calculate second harden slope position or not
CalSPSI = False                                         ## calculate SPSI (Slope Position Sequence Index) or not, Be Caution, only when CalSecHardSlpPos is True, CalSPSI can be True
SPSImethod = 1                                          ## only when CalSPSI is True, the SPSImethod would be used. It can be 1,2,3
DistanceExponentForIDW = 8                              ## the default is 8
