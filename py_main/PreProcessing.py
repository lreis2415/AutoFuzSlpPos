#! /usr/bin/env python
# coding=utf-8
# @Description: Calculate terrain attributes from DEM and other optional inputs for deriving slope position.
#               Slope, Curvature, RPI, HAND, etc.
# @Author:  Liang-Jun Zhu
#
import time
from shutil import copy2
import TauDEM
from Nomenclature import *
from Util import *
from RidgeExtraction import findRidge


def PreProcessing(model):
    startT = time.time()
    logStatus = open(log_preproc, 'w')
    if model == 0:
        logStatus.write("Preprocessing based on D8 flow model.\n")
    elif model == 1:
        logStatus.write("Preprocessing based on D-infinity flow model.\n")
    logStatus.flush()
    logStatus.write("[Preprocessing] [1/7] Converting DEM file format to GeoTiff...\n")
    logStatus.flush()
    Raster2GeoTIFF(rawdem, dem)
    logStatus.write("[Preprocessing] [2/7] Removing pits...\n")
    logStatus.flush()
    TauDEM.pitremove(dem, inputProc, demfil, mpiexeDir = mpiexeDir, exeDir = exeDir,
                     hostfile = hostfile)  # pitremove in TauDEM
    logStatus.write("[Preprocessing] [3/7] Flow direction and slope in radian...\n")
    logStatus.flush()
    TauDEM.D8FlowDir(demfil, inputProc, D8FlowDir, D8Slp, mpiexeDir = mpiexeDir, exeDir = exeDir, hostfile = hostfile)

    if model == 1:
        TauDEM.DinfFlowDir(demfil, inputProc, DinfFlowDir, DinfSlp, mpiexeDir = mpiexeDir, exeDir = exeDir,
                           hostfile = hostfile)
    logStatus.write("[Preprocessing] [4/7] Generating flow accumulation...\n")
    logStatus.flush()
    #  flow accumulation without weight grid or outlet
    TauDEM.AreaD8(D8FlowDir, '', '', 'false', inputProc, D8ContriArea, mpiexeDir = mpiexeDir, exeDir = exeDir,
                  hostfile = hostfile)
    global D8StreamThreshold
    if D8StreamThreshold > 0:
        TauDEM.Threshold(D8ContriArea, '', D8StreamThreshold, inputProc, D8Stream, mpiexeDir = mpiexeDir,
                         exeDir = exeDir, hostfile = hostfile)
    else:
        #  initial stream
        maxAccum, minAccum, meanAccum, STDAccum = GetRasterStat(D8ContriArea)
        TauDEM.Threshold(D8ContriArea, '', meanAccum, inputProc, D8Stream, mpiexeDir = mpiexeDir,
                         exeDir = exeDir, hostfile = hostfile)
    global outlet
    if outlet is None:
        TauDEM.ConnectDown(D8ContriArea, outletpre, inputProc, mpiexeDir = mpiexeDir, exeDir = exeDir,
                           hostfile = hostfile)
        outlet = outletpre
    TauDEM.MoveOutletsToStreams(D8FlowDir, D8Stream, outlet, maxMoveDist, inputProc, outletM, mpiexeDir = mpiexeDir,
                                exeDir = exeDir, hostfile = hostfile)
    if model == 0:
        logStatus.write("[Preprocessing] [5/7] Generating stream source raster based on Drop Analysis...\n")
    elif model == 1:
        logStatus.write(
                "[Preprocessing] [5/7] Generating stream source raster based on Threshold derived from D8 flow model drop analysis or assigned...\n")
    logStatus.flush()
    if model == 1:
        TauDEM.AreaDinf(DinfFlowDir, '', '', 'false', inputProc, DinfContriArea, mpiexeDir = mpiexeDir, exeDir = exeDir,
                        hostfile = hostfile)
    #  ReCalculate flow accumulation using PkrDglStream as weight grid
    if D8StreamThreshold <= 0:
        TauDEM.StreamSkeleton(demfil, PkrDglStream, inputProc, mpiexeDir = mpiexeDir, exeDir = exeDir,
                              hostfile = hostfile)
        TauDEM.AreaD8(D8FlowDir, '', PkrDglStream, 'false', inputProc, D8ContriArea, mpiexeDir = mpiexeDir,
                      exeDir = exeDir, hostfile = hostfile)
        maxAccum, minAccum, meanAccum, STDAccum = GetRasterStat(D8ContriArea)

        if meanAccum - 1.39 * STDAccum < 0:
            minthresh = meanAccum
        else:
            minthresh = meanAccum - 1.39 * STDAccum
        maxthresh = meanAccum + 1.39 * STDAccum

        TauDEM.DropAnalysis(demfil, D8FlowDir, D8ContriArea, D8ContriArea, outletM, minthresh, maxthresh, numthresh,
                            logspace, inputProc, drpFile, mpiexeDir = mpiexeDir, exeDir = exeDir,
                            hostfile = hostfile)
        drpf = open(drpFile, "r")
        tempContents = drpf.read()
        (beg, d8drpThreshold) = tempContents.rsplit(' ', 1)
        drpf.close()
        D8StreamThreshold = d8drpThreshold

        TauDEM.Threshold(D8ContriArea, '', D8StreamThreshold, inputProc, D8Stream,
                         mpiexeDir = mpiexeDir, exeDir = exeDir, hostfile = hostfile)
    if model == 1:
        global DinfStreamThreshold
        if DinfStreamThreshold == 0:
            DinfStreamThreshold = D8StreamThreshold
        TauDEM.Threshold(DinfContriArea, '', DinfStreamThreshold, inputProc, DinfStream, mpiexeDir = mpiexeDir,
                         exeDir = exeDir, hostfile = hostfile)
    logStatus.write("[Preprocessing] [6/7] Calculating RPI(Relative Position Index)...\n")
    logStatus.flush()
    if model == 0:  # D8 model
        #  HAND
        TauDEM.D8DistDownToStream(D8FlowDir, demfil, D8Stream, D8DistDown_V, 'vertical', D8StreamTag, inputProc,
                                  mpiexeDir = mpiexeDir, exeDir = exeDir, hostfile = hostfile)
        if rpiMethod == 1:  # calculate RPI based on hydrological proximity measures (Default).
            TauDEM.D8DistDownToStream(D8FlowDir, demfil, D8Stream, D8DistDown, D8DownMethod, D8StreamTag, inputProc,
                                      mpiexeDir = mpiexeDir, exeDir = exeDir, hostfile = hostfile)
            TauDEM.D8DistUpToRidge(D8FlowDir, demfil, D8DistUp, D8UpMethod, D8UpStats, inputProc, rdg = RdgSrc,
                                   mpiexeDir = mpiexeDir, exeDir = exeDir, hostfile = hostfile)
            TauDEM.SimpleCalculator(D8DistDown, D8DistUp, RPID8, 4, inputProc, mpiexeDir = mpiexeDir, exeDir = exeDir,
                                    hostfile = hostfile)
    elif model == 1:  # Dinf model
        #  HAND
        TauDEM.DinfDistDown(DinfFlowDir, demfil, D8Stream, DinfDownStat, 'vertical', 'false', DinfDistDownWG,
                            inputProc, DinfDistDown_V, mpiexeDir = mpiexeDir, exeDir = exeDir, hostfile = hostfile)
        if rpiMethod == 1:
            TauDEM.DinfDistDown(DinfFlowDir, demfil, D8Stream, DinfDownStat, DinfDownMethod, 'false', DinfDistDownWG,
                                inputProc, DinfDistDown, mpiexeDir = mpiexeDir, exeDir = exeDir, hostfile = hostfile)
            TauDEM.DinfDistUpToRidge(DinfFlowDir, demfil, DinfSlp, propthresh, DinfUpStat, DinfUpMethod, 'false',
                                     inputProc, DinfDistUp, rdg = RdgSrc, mpiexeDir = mpiexeDir, exeDir = exeDir,
                                     hostfile = hostfile)
            TauDEM.SimpleCalculator(DinfDistDown, DinfDistUp, RPIDinf, 4, inputProc, mpiexeDir = mpiexeDir,
                                    exeDir = exeDir, hostfile = hostfile)
    if rpiMethod == 0:  # calculate RPI based on Skidmore's method
        TauDEM.StreamNet(demfil, D8FlowDir, D8ContriArea, D8Stream, outletM, D8StreamOrd, NetTree, NetCoord,
                         D8StreamNet, SubBasin, inputProc, mpiexeDir = mpiexeDir, exeDir = exeDir, hostfile = hostfile)
        if VlySrcCal is None or not isFileExists(VlySrcCal):
            copy2(D8Stream, VlySrcCal)
        if RdgSrcCal is None or not isFileExists(RdgSrcCal):
            findRidge(1, eliminateCount, RdgSrcCal)
        TauDEM.RPISkidmore(VlySrcCal, RdgSrcCal, RPISkidmore, inputProc, 1, 1, dist2Vly, dist2Rdg,
                           mpiexeDir = mpiexeDir, exeDir = exeDir, hostfile = hostfile)
    logStatus.write("[Preprocessing] [7/7] Calculating Plan Curvature and Profile Curvature...\n")
    logStatus.flush()
    TauDEM.Curvature(inputProc, demfil, prof = ProfC, horiz = HorizC, mpiexeDir = mpiexeDir, exeDir = exeDir,
                     hostfile = hostfile)

    if model == 0:
        slopeTrans(D8Slp, Slope)
        if rpiMethod == 1:
            copy2(RPID8, RPI)
        else:
            copy2(RPISkidmore, RPI)
        copy2(D8DistDown_V, HAND)
    elif model == 1:
        slopeTrans(DinfSlp, Slope)
        if rpiMethod == 1:
            copy2(RPIDinf, RPI)
        else:
            copy2(RPISkidmore, RPI)
        copy2(DinfDistDown_V, HAND)
    logStatus.write("[Preprocessing] Preprocessing succeed!\n")
    logStatus.flush()
    endT = time.time()
    cost = (endT - startT) / 60.
    logStatus.write("Time consuming: %.2f min.\n" % cost)
    logStatus.flush()
    logStatus.close()


if __name__ == '__main__':
    ini, proc, root = GetInputArgs()
    LoadConfiguration(ini, proc, root)
    PreProcessing(FlowModel)
