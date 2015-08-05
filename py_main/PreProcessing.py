#! /usr/bin/env python
#coding=utf-8
# Revised: 5/12/2015  Removing 

from Nomenclature import *
from Util import *
import TauDEM
import time
from Config import *
from shutil import copy2
# Stage 1: Preprocessing for Slope, Curvature, RPI
def PreProcessing(model):
    startT = time.time()
    logStatus = open(log_preproc, 'w')
    if model == 0:
        logStatus.write("Preprocessing based on D8 flow model.\n")
    elif model ==1:
        logStatus.write("Preprocessing based on D-infinity flow model.\n")
    logStatus.flush()
    logStatus.write("[Preprocessing] [1/7] Converting DEM file format to GeoTiff...\n")
    logStatus.flush()
    TIFF2GeoTIFF(rawdem, dem)
    logStatus.write("[Preprocessing] [2/7] Removing pits...\n")
    logStatus.flush()
    #TauDEM.pitremoveplanchon(dem,deltaElev,1,demfilpre,mpiexeDir=mpiexeDir,exeDir=exeDir)
    #TauDEM.pitremove(demfilpre,inputProc,demfil,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile) # pitremove in TauDEM
    TauDEM.pitremove(dem,inputProc,demfil,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile) # pitremove in TauDEM
    logStatus.write("[Preprocessing] [3/7] Flow direction and slope in radian...\n")
    logStatus.flush()
    TauDEM.D8FlowDir(demfil,inputProc,D8FlowDir,D8Slp,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)

    if model == 1:
        TauDEM.DinfFlowDir(demfil,inputProc,DinfFlowDir,DinfSlp,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
    logStatus.write("[Preprocessing] [4/7] Generating flow accumulation...\n")
    logStatus.flush()  
    TauDEM.AreaD8(D8FlowDir,'','','false',inputProc,D8ContriArea,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
    maxAccum, minAccum, meanAccum, STDAccum = GetRasterStat(D8ContriArea)
    TauDEM.Threshold(D8ContriArea,'',meanAccum,inputProc,D8Stream,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
    global outlet
    if outlet is None:
        TauDEM.ConnectDown(D8ContriArea,outletpre,inputProc,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
        outlet = outletpre
    TauDEM.MoveOutletsToStreams(D8FlowDir,D8Stream,outlet,maxMoveDist,inputProc,outletM, mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)

    if model == 1:
        TauDEM.AreaDinf(DinfFlowDir,'','','false',inputProc,DinfContriArea,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
    if model ==0:
        logStatus.write("[Preprocessing] [5/7] Generating stream source raster based on Drop Analysis...\n")
    elif model == 1:
        logStatus.write("[Preprocessing] [5/7] Generating stream source raster based on Threshold derived from D8 flow model drop analysis or assigned...\n")
    logStatus.flush()
    global D8StreamThreshold
    if D8StreamThreshold == 0:
        ## both D8 and D-infinity need to run drop analysis
        maxAccum, minAccum, meanAccum, STDAccum = GetRasterStat(D8ContriArea) #print maxAccum, minAccum, meanAccum, STDAccum
        if meanAccum - STDAccum < 0:
            minthresh = meanAccum
        else:
            minthresh = meanAccum - STDAccum
        maxthresh = meanAccum + STDAccum
        if outlet is not None:
            TauDEM.DropAnalysis(demfil,D8FlowDir,D8ContriArea,D8ContriArea,outletM,minthresh,maxthresh,numthresh,logspace,inputProc,drpFile, mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
            drpf = open(drpFile,"r")
            tempContents=drpf.read()
            (beg,d8drpThreshold)=tempContents.rsplit(' ',1)
            drpf.close()
            D8StreamThreshold = d8drpThreshold
        else:
            D8StreamThreshold = minthresh + (maxthresh - minthresh) * 0.1
    TauDEM.Threshold(D8ContriArea,'',D8StreamThreshold,inputProc,D8Stream,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
    if model == 1:
        global DinfStreamThreshold
        if DinfStreamThreshold == 0:
            DinfStreamThreshold = D8StreamThreshold
        TauDEM.Threshold(DinfContriArea,'',DinfStreamThreshold,inputProc,DinfStream,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
    logStatus.write("[Preprocessing] [6/7] Calculating RPI(Relative Position Index)...\n")
    logStatus.flush()
    if model == 0:
        TauDEM.D8DistDownToStream(D8FlowDir,demfil,D8Stream,D8DistDown,D8DownMethod,D8StreamTag,inputProc,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
        TauDEM.D8DistUpToRidge(D8FlowDir,demfil,D8DistUp,D8UpMethod,D8UpStats,inputProc,rdg=rdgsrc,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
        TauDEM.D8DistDownToStream(D8FlowDir,demfil,D8Stream,D8DistDown_V,'Vertical',D8StreamTag,inputProc,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
        TauDEM.SimpleCalculator(D8DistDown,D8DistUp,RPID8,4,inputProc,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
    elif model == 1:
        #TauDEM.DinfDistDown(DinfFlowDir,demfil,DinfStream,DinfDownStat,DinfDownMethod,'false',DinfDistDownWG,inputProc,DinfDistDown,exeDir=exeDir)
        TauDEM.DinfDistDown(DinfFlowDir,demfil,D8Stream,DinfDownStat,DinfDownMethod,'false',DinfDistDownWG,inputProc,DinfDistDown,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
        TauDEM.DinfDistUpToRidge(DinfFlowDir,demfil,DinfSlp,propthresh,DinfUpStat,DinfUpMethod,'false',inputProc,DinfDistUp,rdg=rdgsrc,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
        TauDEM.DinfDistDown(DinfFlowDir,demfil,D8Stream,DinfDownStat,'Vertical','false',DinfDistDownWG,inputProc,DinfDistDown_V,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)
        TauDEM.SimpleCalculator(DinfDistDown, DinfDistUp, RPIDinf, 4,inputProc,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)

    logStatus.write("[Preprocessing] [7/7] Calculating Plan Curvature and Profile Curvature...\n")
    logStatus.flush()
    TauDEM.Curvature(inputProc,demfil,prof=ProfC,horiz=HorizC,mpiexeDir=mpiexeDir,exeDir=exeDir,hostfile=hostfile)

    if model == 0:
        slopeTrans(D8Slp,Slope)
        #copy2(D8Slp,Slope)
        copy2(RPID8,RPI)
        copy2(D8DistDown_V,HAND)
    elif model == 1:
        slopeTrans(DinfSlp,Slope)
        #copy2(DinfSlp,Slope)
        copy2(RPIDinf,RPI)
        copy2(DinfDistDown_V,HAND)
    logStatus.write("[Preprocessing] Preprocessing succeed!\n")
    logStatus.flush()
    endT = time.time()
    cost = (endT - startT)/60.
    logStatus.write("Time consuming: %.2f min.\n" % cost)
    logStatus.flush()
    logStatus.close()