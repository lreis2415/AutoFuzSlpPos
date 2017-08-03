#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Extensions based on TauDEM framework.

    @author   : Liangjun Zhu

    @changelog: 17-08-01  lj - initial implementation based on pygeoc.\n
"""

import os

from autofuzslppos.pygeoc.pygeoc.hydro.TauDEM import TauDEM
from autofuzslppos.pygeoc.pygeoc.utils.utils import StringClass


class TauDEMExtension(TauDEM):
    """Extension functions based on TauDEM."""

    def __init__(self):
        """Initialize TauDEM."""
        TauDEM.__init__(self)

    @staticmethod
    def d8distuptoridge(np, workingdir, p, fel, src, dist, distancemethod, thresh,
                        mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run D8 distance to stream"""
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('d8distdowntostream', exedir),
                          {'-fel': fel, '-p': p, '-src': src},
                          {'-thresh': thresh, '-m': distancemethod},
                          {'-dist': dist}, {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def dinfdistuptoridge(np, workingdir, ang, fel, slp, propthresh, dist, statsm, distm,
                          edgecontamination, rdg=None,
                          mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run Dinf distance to ridge."""
        os.chdir(workingdir)
        in_params = {'-thresh': str(propthresh),
                     '-m': '%s %s' % (TauDEM.convertstatsmethod(statsm),
                                      TauDEM.convertdistmethod(distm))}
        if StringClass.string_match(edgecontamination, 'false') or edgecontamination is False:
            in_params['-nc'] = None
        return TauDEM.run(TauDEM.fullpath('dinfdistuptoridge', exedir),
                          {'-ang': ang, '-fel': fel, '-slp': slp, '-rdg': rdg},
                          in_params,
                          {'-dist': dist}, {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def extractridge(np, workingdir, angfile, elevfile, rdgsrc,
                     mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Extract ridge source."""
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('ridgeextraction', exedir),
                          {'-dir': angfile, '-fel': elevfile},
                          None,
                          {'-src': rdgsrc},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def rpiskidmore(np, workingdir, vlysrc, rdgsrc, rpi, vlytag=1, rdgtag=1, dist2vly=None,
                    dist2rdg=None, mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Calculate RPI according to Skidmore (1990)."""
        os.chdir(workingdir)
        in_params = dict()
        if vlytag > 0:
            in_params['-vlytag'] = vlytag
        if rdgtag > 0:
            in_params['-rdgtag'] = rdgtag
        return TauDEM.run(TauDEM.fullpath('rpiskidmore', exedir),
                          {'-vly': vlysrc, '-rdg': rdgsrc},
                          in_params,
                          {'-rpi': rpi, '-dist2vly': dist2vly, '-dist2rdg': dist2rdg},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def curvature(np, workingdir, fel, profc, planc=None, horizc=None, unspherc=None, avec=None,
                  maxc=None, minc=None, mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Calculate various curvature."""
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('curvature', exedir),
                          {'-fel': fel}, None,
                          {'-out -prof': profc, '-plan': planc, '-horiz': horizc,
                           '-unspher': unspherc, '-ave': avec, '-max': maxc, '-min': minc},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def simplecalculator(np, workingdir, inputa, inputb, output, operator,
                         mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run simple calculator.

           operator = 0: add
                      1: minus
                      2: multiply
                      3: divide
                      4: a/(a+b)
                      5: mask
        """
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('simplecalculator', exedir),
                          {'-in': [inputa, inputb]},
                          {'-op': operator},
                          {'-out': output},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def selecttyplocslppos(np, workingdir, inputconf, outputconf, extlog=None,
                           mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Select typical locations."""
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('selecttyplocslppos', exedir),
                          {'-in': inputconf}, None,
                          {'-out': outputconf, '-extlog': extlog},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def fuzzyslpposinference(np, workingdir, config, mpiexedir=None,
                             exedir=None, log_file=None, hostfile=None):
        """Run fuzzy inference."""
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('fuzzyslpposinference', exedir),
                          {'-in': config}, None, None,
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def hardenslppos(np, workingdir, simifiles, tags, hard, maxsimi,
                     sechard=None, secsimi=None, spsim=None, spsi=None,
                     mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Select typical locations."""
        os.chdir(workingdir)
        if len(simifiles) != len(tags):
            raise RuntimeError("hardenslppos: simifiles and tags must have the same size!")
        tag_path = ''
        for i, tag in tags:
            tag_path += ' %d %s ' % (tag, simifiles[i])
        in_params = dict()
        if spsim is not None and spsi is not None:
            in_params['-m'] = '%d %s' % (spsim, spsi)
        return TauDEM.run(TauDEM.fullpath('hardenslppos', exedir),
                          {'-inf': '%d %s' % (len(simifiles), tag_path)},
                          in_params,
                          {'-maxS': [hard, maxsimi], '-secS': [sechard, secsimi]},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

# ## Write log
# def outputLog(title, lines):
#     abortRun(title, lines)
#     contentList = []
#     timeDict = {'name': None, 'readt': 0, 'writet': 0, 'computet': 0, 'totalt': 0}
#     timeDict['name'] = title
#     contentList.append('\n')
#     contentList.append("#### %s ####" % title)
#     for line in lines:
#         contentList.append(line.split(LF)[0])
#         # print line
#         if line.find("Read time") >= 0:
#             timeDict['readt'] = line.split(LF)[0].split(':')[-1]
#         elif line.find("Compute time") >= 0:
#             timeDict['computet'] = line.split(LF)[0].split(':')[-1]
#         elif line.find("Write time") >= 0:
#             timeDict['writet'] = line.split(LF)[0].split(':')[-1]
#         elif line.find("Total time") >= 0:
#             timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
#     write_log(Log_all, contentList)
#     write_time_log(Log_runtime, timeDict)


# def MPIHeader(mpiexeDir, inputProc, hostfile=None):
#     if mpiexeDir is not None:
#         cmd = '"' + mpiexeDir + os.sep + 'mpiexec"'
#     else:
#         cmd = '"mpiexec"'
#     if hostfile is not None:
#         cmd = cmd + ' -f ' + hostfile + ' -n '
#     else:
#         cmd += ' -n '
#     return cmd
#
#
# def abortRun(title, lines):
#     for line in lines:
#         if "ERROR" in line.upper() or 'BAD TERMINATION' in line.upper():
#             raise RuntimeError(title + " failed, please contact the developer!")
#     return True


## Basic Grid Analysis
# def pitremove(inZfile, inputProc, outFile, mpiexeDir = None, exeDir = None, hostfile = None):
#     print "PitRemove......"
#     print "Input Elevation file: " + inZfile
#     print "Input Number of Processes: " + str(inputProc)
#     print "Output Pit Removed Elevation file: " + outFile
#     # Construct the taudem command line.  Put quotes around file names in case there are spaces
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' pitremove -z ' + '"' + inZfile + '"' + ' -fel ' + '"' + outFile + '"'
#     else:
#         cmd = cmd + str(
#                 inputProc) + ' ' + exeDir + os.sep + 'pitremove -z ' + '"' + inZfile + '"' + ' -fel ' + '"' + outFile + '"'
#
#     print "Command Line: " + cmd
#     ##os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("PitRemove", process.stdout.readlines())
#
# def ConnectDown(ad8, outlet, inputProc, mpiexeDir = None, exeDir = None, hostfile = None):
#     print "Generating outlet shapefile from areaD8......"
#     print "Input areaD8 file: " + ad8
#     print "Input Number of Processes: " + str(inputProc)
#     print "Output outlet File: " + outlet
#
#     # Construct command
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' connectdown -ad8 ' + '"' + ad8 + '"' + ' -o ' + '"' + outlet + '"'
#     else:
#         cmd = cmd + str(
#                 inputProc) + ' ' + exeDir + os.sep + 'connectdown -ad8 ' + '"' + ad8 + '"' + ' -o ' + '"' + outlet + '"'
#
#     print "Command Line: " + cmd
#     ##os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("ConnectDown", process.stdout.readlines())
#
#
# def D8FlowDir(fel, inputProc, p, sd8, mpiexeDir = None, exeDir = None, hostfile = None):
#     print "Calculating D8 flow direction......"
#     print "Input Pit Filled Elevation file: " + fel
#     print "Input Number of Processes: " + str(inputProc)
#     print "Output D8 Flow Direction File: " + p
#     print "Output D8 Slope File: " + sd8
#     # Construct command
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' d8flowdir -fel ' + '"' + fel + '"' + ' -p ' + '"' + p + '"' + \
#               ' -sd8 ' + '"' + sd8 + '"'
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'd8flowdir -fel ' + '"' + fel + '"' + ' -p ' + '"' + p +\
#               '"' + ' -sd8 ' + '"' + sd8 + '"'
#
#     print "Command Line: " + cmd
#     ##os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("D8FlowDir", process.stdout.readlines())
#
#
# def DinfFlowDir(fel, inputProc, ang, slp, mpiexeDir = None, exeDir = None, hostfile = None):
#     print "Calculating D-infinity direction......"
#     print "Input Pit Filled Elevation file: " + fel
#     print "Input Number of Processes: " + str(inputProc)
#     print "Output Dinf Flow Direction File: " + ang
#     print "Output Dinf Slope File: " + slp
#     # Construct command
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' dinfflowdir -fel ' + '"' + fel + '"' + ' -ang ' + '"' + ang + '"' +\
#               ' -slp ' + '"' + slp + '"'
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'dinfflowdir -fel ' + '"' + fel + '"' + ' -ang ' +\
#               '"' + ang + '"' + ' -slp ' + '"' + slp + '"'
#
#     print "Command Line: " + cmd
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("DinfFlowDir", process.stdout.readlines())
#
#
# def AreaD8(p, Shapefile, weightgrid, edgecontamination, inputProc, ad8, mpiexeDir = None, exeDir = None,
#            hostfile = None):
#     print "Calculating D8 contributing area......"
#     print "Input D8 Flow Direction file: " + p
#     if os.path.exists(Shapefile):
#         print "Input Outlets Shapefile: " + Shapefile
#     if os.path.exists(weightgrid):
#         print "Input Weight Grid: " + weightgrid
#     print "Edge Contamination: " + edgecontamination
#     print "Input Number of Processes: " + str(inputProc)
#     print "Output D8 Contributing Area Grid: " + ad8
#     # Construct command
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' aread8 -p ' + '"' + p + '"' + ' -ad8 ' + '"' + ad8 + '"'
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'aread8 -p ' + '"' + p + '"' + ' -ad8 ' + '"' + ad8 + '"'
#     if os.path.exists(Shapefile):
#         cmd = cmd + ' -o ' + '"' + Shapefile + '"'
#     if os.path.exists(weightgrid):
#         cmd = cmd + ' -wg ' + '"' + weightgrid + '"'
#     if StringMatch(edgecontamination, 'false') or edgecontamination is False:
#         cmd += ' -nc '
#
#     print "Command Line: " + cmd
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("D8 contributing area", process.stdout.readlines())
#
#
# def AreaDinf(ang, shapefile, weightgrid, edgecontamination, inputProc, sca, mpiexeDir = None, exeDir = None,
#              hostfile = None):
#     print "Calculating D-infinity contributing area......"
#     print "Input Dinf Flow Direction file: " + ang
#     if os.path.exists(shapefile):
#         print "Input Outlets Shapefile: " + shapefile
#     if os.path.exists(weightgrid):
#         print "Input Weight Grid: " + weightgrid
#     print "Edge Contamination: " + edgecontamination
#     print "Input Number of Processes: " + str(inputProc)
#     print "Output Dinf Specific Catchment Area Grid: " + sca
#     # Construct command
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' areadinf -ang ' + '"' + ang + '"' + ' -sca ' + '"' + sca + '"'
#     else:
#         cmd = cmd + str(
#                 inputProc) + ' ' + exeDir + os.sep + 'areadinf -ang ' + '"' + ang + '"' + ' -sca ' + '"' + sca + '"'
#     if os.path.exists(shapefile):
#         cmd = cmd + ' -o ' + '"' + shapefile + '"'
#     if os.path.exists(weightgrid):
#         cmd = cmd + ' -wg ' + '"' + weightgrid + '"'
#     if StringMatch(edgecontamination, 'false') or edgecontamination is False:
#         cmd += ' -nc '
#
#     print "Command Line: " + cmd
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("D-inf contributing area", process.stdout.readlines())
#
#
# ## Specialized grid analysis
#
# def DinfDistDown(ang, fel, src, statisticalmethod, distancemethod, edgecontamination, wg, inputProc, dd,
#                  mpiexeDir = None, exeDir = None, hostfile = None):
#     print "Calculating distance down to stream based on D-infinity model......"
#     print "Input D-Infinity Flow Direction Grid: " + ang
#     print "Input Pit Filled Elevation Grid: " + fel
#     print "Input Stream Raster Grid: " + src
#     print "Statistical Method: " + statisticalmethod
#     print "Distance Method: " + distancemethod
#     print "Edge Contamination: " + edgecontamination
#     if wg is not None and os.path.exists(wg):
#         print "Input Weight Path Grid: " + wg
#     print "Input Number of Processes: " + str(inputProc)
#     print "Output D-Infinity Drop to Stream Grid: " + dd
#
#     # Construct command
#     if StringMatch(statisticalmethod, 'Average'):
#         statmeth = 'ave'
#     elif StringMatch(statisticalmethod, 'Maximum'):
#         statmeth = 'max'
#     elif StringMatch(statisticalmethod,'Minimum'):
#         statmeth = 'min'
#     else:
#         statmeth = 'ave'
#     if StringMatch(distancemethod, 'Horizontal'):
#         distmeth = 'h'
#     elif StringMatch(distancemethod, 'Vertical'):
#         distmeth = 'v'
#     elif StringMatch(distancemethod, 'Pythagoras'):
#         distmeth = 'p'
#     elif StringMatch(distancemethod, 'Surface'):
#         distmeth = 's'
#     else:
#         distmeth = 's'
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' dinfdistdown -fel ' + '"' + fel + '"' + ' -ang ' + '"' + ang + '"' + \
#               ' -src ' + '"' + src + '"' + ' -dd ' + '"' + dd + '"' + ' -m ' + statmeth + ' ' + distmeth
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'dinfdistdown -fel ' + '"' + fel + '"' + \
#               ' -ang ' + '"' + ang + '"' + ' -src ' + '"' + src + '"' + ' -dd ' + '"' + dd + '"' + ' -m ' + \
#               statmeth + ' ' + distmeth
#
#     if wg is not None and os.path.exists(wg):
#         cmd = cmd + ' -wg ' + '"' + wg + '"'
#     if StringMatch(edgecontamination, 'false') or edgecontamination is False:
#         cmd += ' -nc '
#
#     print "Command Line: " + cmd
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("Dinf distance down", process.stdout.readlines())
#
#
# def MoveOutletsToStreams(p, src, shapefile, maxdistance, inputProc, om, mpiexeDir = None, exeDir = None,
#                          hostfile = None):
#     print "Moving outlet point(s) to streams......"
#     print "Input D8 Flow Direction Grid: " + p
#     print "Input Stream Raster Grid: " + src
#     print "Input Outlets Shapefile: " + shapefile
#     print "Minimum Threshold Value: " + str(maxdistance)
#     print "Input Number of Processes: " + str(inputProc)
#
#     print "Output Outlet Shapefile: " + om
#
#     # Construct command
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' moveoutletstostreams -p ' + '"' + p + '"' + ' -src ' + '"' + src + \
#               '"' + ' -o ' + '"' + shapefile + '"' + ' -om ' + '"' + om + '"' + ' -md ' + str(maxdistance)
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'moveoutletstostreams -p ' + '"' + p + '"' + \
#               ' -src ' + '"' + src + '"' + ' -o ' + '"' + shapefile + '"' + ' -om ' + '"' + om + '"' + \
#               ' -md ' + str(maxdistance)
#
#     print "Command Line: " + cmd
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("Moving outlet point to streams", process.stdout.readlines())
#
# def StreamNet(filledDem, flowDir, acc, streamRaster, modifiedOutlet, streamOrder, chNetwork, chCoord,
#               streamNet, subbasin,inputProc, mpiexeDir = None, exeDir = None,hostfile = None):
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#     if exeDir is not None:
#         exe = exeDir + os.sep + "streamnet"
#     else:
#         exe = "streamnet"
#     cmd += " %d %s -fel %s -p %s -ad8 %s -src %s -o %s  -ord %s -tree %s -coord %s -net %s -w %s" % (
#         inputProc, exe, filledDem, flowDir, acc, streamRaster, modifiedOutlet, streamOrder, chNetwork, chCoord,
#         streamNet, subbasin)
#
#     print cmd
#     process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#     outputLog("Stream net", process.stdout.readlines())
#
# def Threshold(ssa, mask, threshold, inputProc, src, mpiexeDir = None, exeDir = None, hostfile = None):
#     print "Stream definition according to threshold......"
#     print "Input Accumulated Stream Source Grid: " + ssa
#     if os.path.exists(mask):
#         print "Input Mask Grid: " + mask
#     print "Threshold: " + str(threshold)
#     print "Input Number of Processes: " + str(inputProc)
#
#     print "Output Stream Raster Grid: " + src
#
#     # Construct command
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' threshold -ssa ' + '"' + ssa + '"' + ' -src ' + '"' + src + '"' + \
#               ' -thresh ' + str(threshold)
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'threshold -ssa ' + '"' + ssa + '"' + ' -src ' + \
#               '"' + src + '"' + ' -thresh ' + str(threshold)
#
#     if os.path.exists(mask):
#         cmd = cmd + ' -mask ' + mask
#
#     print "Command Line: " + cmd
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("Threshold to define stream", process.stdout.readlines())
#
# def StreamSkeleton(filledDem, streamSkeleton, inputProc, mpiexeDir=None, exeDir=None, hostfile = None):
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#     if exeDir is not None:
#         exe = exeDir + os.sep + "peukerdouglas"
#     else:
#         exe = "peukerdouglas"
#     cmd += "%d %s -fel %s -ss %s" % (inputProc, exe, filledDem, streamSkeleton)
#
#     print cmd
#     process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#     outputLog("Stream skeleton based on Peuker-Douglas", process.stdout.readlines())
#
# def DropAnalysis(fel, p, ad8, ssa, shapefile, minthresh, maxthresh, numthresh, logspace, inputProc, drp,
#                  mpiexeDir = None, exeDir = None, hostfile = None):
#     print "Stream drop analysis for the optimal threshold......"
#     print "Input Pit Filled Elevation Grid: " + fel
#     print "Input D8 Flow Direction Grid: " + p
#     print "Input D8 Contributing Area Grid: " + ad8
#     print "Input Accumulated Stream Source Grid: " + ssa
#     print "Input Outlets Shapefile: " + shapefile
#     print "Minimum Threshold Value: " + str(minthresh)
#     print "Maximum Threshold Value: " + str(maxthresh)
#     print "Number of Threshold Values: " + str(numthresh)
#     if logspace:
#         print "Spacing method: logarithmic spacing"
#     else:
#         print "Spacing method: linear spacing"
#     print "Input Number of Processes: " + str(inputProc)
#
#     print "Output Drop Analysis Text File: " + drp
#
#     # Construct command
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' dropanalysis -fel ' + '"' + fel + '"' + ' -p ' + '"' + p + '"' + ' -ad8 ' +\
#               '"' + ad8 + '"' + ' -ssa ' + '"' + ssa + '"' + ' -o ' + '"' + shapefile + '"' + ' -drp ' + '"' + drp + \
#               '"' + ' -par ' + str(minthresh) + ' ' + str(maxthresh) + ' ' + str(numthresh) + ' '
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'dropanalysis -fel ' + '"' + fel + '"' + ' -p ' + \
#               '"' + p + '"' + ' -ad8 ' + '"' + ad8 + '"' + ' -ssa ' + '"' + ssa + '"' + ' -o ' + '"' + shapefile + \
#               '"' + ' -drp ' + '"' + drp + '"' + ' -par ' + str(minthresh) + ' ' + str(maxthresh) + ' ' +\
#               str(numthresh) + ' '
#     if logspace:
#         cmd += '0'
#     else:
#         cmd += '1'
#
#     print "Command Line: " + cmd
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("Drop analysis", process.stdout.readlines())
#
#
# ####   Functions added by Liangjun Zhu    ####
#
# def D8DistDownToStream(p, fel, src, dist, distancemethod, thresh, inputProc, mpiexeDir = None, exeDir = None,
#                        hostfile = None):
#     print "Calculating distance down to stream based on D8 model......"
#     print "Input D8 Flow Direction Grid: " + p
#     print "Input filled DEM: " + fel
#     print "Input Stream Raster Grid: " + src
#     print "Distance calculating method: " + distancemethod
#     print "Threshold: " + str(thresh)
#     print "Input Number of Processes: " + str(inputProc)
#     print "Output Distance To Streams: " + dist
#     if StringMatch(distancemethod, 'Horizontal'):
#         distmeth = 'h'
#     elif StringMatch(distancemethod, 'Vertical'):
#         distmeth = 'v'
#     elif StringMatch(distancemethod, 'Pythagoras'):
#         distmeth = 'p'
#     elif StringMatch(distancemethod, 'Surface'):
#         distmeth = 's'
#     else:
#         distmeth = 's'
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' d8distdowntostream -p ' + '"' + p + '"' + ' -fel ' + '"' + fel + '"' + \
#               ' -src ' + '"' + src + '"' + ' -dist ' + '"' + dist + '"' + ' -m ' + distmeth + ' -thresh ' + str(thresh)
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'd8distdowntostream -p ' + '"' + p + '"' + ' -fel ' + \
#               '"' + fel + '"' + ' -src ' + '"' + src + '"' + ' -dist ' + '"' + dist + '"' + ' -m ' + distmeth + \
#               ' -thresh ' + str(thresh)
#
#     print "Command Line: " + cmd
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
#     outputLog("D8 distance down", process.stdout.readlines())
#
#
# def D8DistUpToRidge(p, fel, du, distancemethod, statisticalmethod, inputProc, rdg=None,
#                     mpiexeDir=None,
#                     exeDir=None, hostfile=None):
#     print "Calculating distance up to ridges based on D8 model......"
#     print "Input D8 Flow Direction Grid: " + p
#     print "Input Pit Filled Elevation Grid: " + fel
#     if not rdg is None:
#         print "Input Ridge Source Grid: " + rdg
#     print "Statistical Method: " + statisticalmethod
#     print "Distance Method: " + distancemethod
#     print "Input Number of Processes: " + str(inputProc)
#     print "Output D-Infinity Distance Up: " + du
#
#     # Construct command
#     if StringMatch(statisticalmethod, 'Average'):
#         statmeth = 'ave'
#     elif StringMatch(statisticalmethod, 'Maximum'):
#         statmeth = 'max'
#     elif StringMatch(statisticalmethod, 'Minimum'):
#         statmeth = 'min'
#     else:
#         statmeth = 'ave'
#     if StringMatch(distancemethod, 'Horizontal'):
#         distmeth = 'h'
#     elif StringMatch(distancemethod, 'Vertical'):
#         distmeth = 'v'
#     elif StringMatch(distancemethod, 'Pythagoras'):
#         distmeth = 'p'
#     elif StringMatch(distancemethod, 'Surface'):
#         distmeth = 's'
#     else:
#         distmeth = 's'
#
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' d8distuptoridge -p '
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'd8distuptoridge -p '
#     if not rdg is None:
#         cmd = cmd + '"' + p + '"' + ' -fel ' + '"' + fel + '"' + ' -rdg ' + '"' + rdg + '"' + ' -du ' + '"' + du + \
#               '"' + ' -m ' + statmeth + ' ' + distmeth
#     else:
#         cmd = cmd + '"' + p + '"' + ' -fel ' + '"' + fel + '"' + ' -du ' + '"' + du + '"' + ' -m ' + statmeth + \
#               ' ' + distmeth
#
#     print "Command Line: " + cmd
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#     outputLog("D8 distance up", process.stdout.readlines())
#

# def DinfDistUpToRidge(ang, fel, slp, propthresh, statisticalmethod, distancemethod,
#                       edgecontamination, inputProc, du,
#                       rdg=None, mpiexeDir=None, exeDir=None, hostfile=None):
#     print "Calculating distance up to ridges based on D-infinity model......"
#     print "Input D-Infinity Flow Direction Grid: " + ang
#     print "Input Pit Filled Elevation Grid: " + fel
#     print "Input Slope Grid: " + slp
#     if not rdg is None:
#         print "Input Ridge Source Grid: " + rdg
#     print "Input Proportion Threshold: " + str(propthresh)
#     print "Statistical Method: " + statisticalmethod
#     print "Distance Method: " + distancemethod
#     print "Edge Contamination: " + edgecontamination
#     print "Input Number of Processes: " + str(inputProc)
#
#     print "Output D-Infinity Distance Up: " + du
#
#     # Construct command
#     if StringMatch(statisticalmethod, 'Average'):
#         statmeth = 'ave'
#     elif StringMatch(statisticalmethod, 'Maximum'):
#         statmeth = 'max'
#     elif StringMatch(statisticalmethod, 'Minimum'):
#         statmeth = 'min'
#     else:
#         statmeth = 'ave'
#     if StringMatch(distancemethod, 'Horizontal'):
#         distmeth = 'h'
#     elif StringMatch(distancemethod, 'Vertical'):
#         distmeth = 'v'
#     elif StringMatch(distancemethod, 'Pythagoras'):
#         distmeth = 'p'
#     elif StringMatch(distancemethod, 'Surface'):
#         distmeth = 's'
#     else:
#         distmeth = 's'
#
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' dinfdistuptoridge '
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'dinfdistuptoridge '
#     if not rdg is None:
#         cmd = cmd + ' -ang ' + '"' + ang + '"' + ' -fel ' + '"' + fel + '"' + ' -slp ' + '"' + slp + '"' + \
#               ' -rdg ' + '"' + rdg + '"' + ' -du ' + '"' + du + '"' + ' -m ' + statmeth + ' ' + distmeth + \
#               ' -thresh ' + str(propthresh)
#     else:
#         cmd = cmd + ' -ang ' + '"' + ang + '"' + ' -fel ' + '"' + fel + '"' + ' -slp ' + '"' + slp + '"' + \
#               ' -du ' + '"' + du + '"' + ' -m ' + statmeth + ' ' + distmeth + ' -thresh ' + str(
#             propthresh)
#     if StringMatch(edgecontamination, 'false') or edgecontamination is False:
#         cmd += ' -nc '
#
#     print "Command Line: " + cmd
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#     outputLog("Dinf distance up", process.stdout.readlines())
#
#
# def Curvature():
#     cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
#
#     if exeDir is None:
#         cmd = cmd + str(inputProc) + ' curvature'
#     else:
#         cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'curvature'
#     if prof is None and plan is None and horiz is None and unspher is None and ave is None and \
#                     max is None and min is None:
#         cmd = cmd + ' -fel ' + '"' + fel + '"'
#     else:
#         cmd = cmd + ' -fel ' + '"' + fel + '"' + ' -out '
#     print "Input Pit Filled Elevation Grid: " + fel
#     if not prof is None:
#         print "Output Profile Curvature Grid: " + prof
#         cmd = cmd + ' -prof ' + '"' + prof + '" '
#     if not plan is None:
#         print "Output Plan Curvature Grid: " + plan
#         cmd = cmd + ' -plan ' + '"' + plan + '" '
#     if not horiz is None:
#         print "Output Horizontal Curvature Grid: " + horiz
#         cmd = cmd + ' -horiz ' + '"' + horiz + '" '
#     if not unspher is None:
#         print "Output Nnsphericity Grid: " + unspher
#         cmd = cmd + ' -unspher ' + '"' + unspher + '" '
#     if not ave is None:
#         print "Output Average Curvature Grid: " + ave
#         cmd = cmd + ' -ave ' + '"' + ave + '" '
#     if not max is None:
#         print "Output Maximum Curvature Grid: " + max
#         cmd = cmd + ' -max ' + '"' + max + '" '
#     if not min is None:
#         print "Output Minimum Curvature Grid: " + min
#         cmd = cmd + ' -min ' + '"' + min + '" '
#
#     print "Command Line: " + cmd
#     print "Input Number of Processes: " + str(inputProc)
#     # os.system(cmd)
#     process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#     outputLog("Curvature", process.stdout.readlines())
#
