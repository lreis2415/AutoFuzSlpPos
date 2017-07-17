#! /usr/bin/env python
# coding=utf-8
# Description: Utility functions.
# Author: Liang-Jun Zhu
#
import argparse
import math
import os
import sys
import subprocess
from shutil import rmtree
import numpy
import re
from gdalconst import *
from osgeo import gdal
from osgeo import ogr
from osgeo import osr

NODATA_VALUE = -9999.
class C(object):
    pass


def GetInputArgs():
    # Get model configuration file name
    c = C()
    parser = argparse.ArgumentParser(description = "Read AutoFuzSlpPos configuration file.")
    parser.add_argument('-ini', help = "Full path of configuration file")
    parser.add_argument('-proc', help="Number of processor for parallel computing "
                                      "which will override inputProc in *.ini file.")
    parser.add_argument('-root', help="Workspace to store results, which will override"
                                      "rootDir in *.ini file.")
    args = parser.parse_args(namespace = c)
    iniFile = args.ini
    inputProc = args.proc
    rootDir = args.root
    if inputProc is not None:
        xx = FindNumberFromString(inputProc)
        if len(xx) != 1:
            raise IOError("-proc MUST be one integer number!")
        inputProc = int(xx[0])
    else:
        inputProc = -1
    if not os.path.exists(iniFile) or iniFile is None:
        raise IOError("%s MUST be provided and existed, please check and retry!" % iniFile)

    return iniFile, inputProc, rootDir


def isPathExists(path):
    if os.path.isdir(path):
        if os.path.exists(path):
            return True
        else:
            return False
    else:
        return False


def isFileExists(filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return True
    else:
        return False


def LoadConfiguration(inifile, proc, root):
    strCmd = '%s %s/Config.py -ini %s' % (sys.executable, currentPath(), inifile)
    if proc > 0:
        strCmd += " -proc %d" % proc
    if root is not None:
        strCmd += ' -root %s' % root
    # print strCmd
    os.system(strCmd)


def currentPath():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def mkdir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def rmmkdir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    else:
        rmtree(dir, True)
        os.mkdir(dir)


def makeResultFolders(rootdir, model, preprocess):
    # print "Making results' folders..."
    if not os.path.isdir(rootdir):
        if rootdir != "":
            mkdir(rootdir)
        else:
            rootdir = currentPath() + os.sep + "FuzzySlpPos"
            mkdir(rootdir)

    if model == 0:
        PreprocessDir = rootdir + os.sep + "D8preDir"
        # negDEMDir = rootdir + os.sep + "negD8Dir"
    else:
        PreprocessDir = rootdir + os.sep + "DinfpreDir"
        # negDEMDir = rootdir + os.sep + "negDinfDir"
    ParamDir = rootdir + os.sep + "Params"  ## contains RPI,Curvature,Slope etc.
    logDir = rootdir + os.sep + "Log"
    outputDir = rootdir + os.sep + "FuzzySlpPos"
    TypLocDir = rootdir + os.sep + "TypLoc"
    ConfDir = rootdir + os.sep + "Config"
    if preprocess:
        mkdir(PreprocessDir)
        # mkdir(negDEMDir)
    mkdir(ParamDir)
    mkdir(outputDir)
    rmmkdir(logDir)
    mkdir(TypLocDir)
    mkdir(ConfDir)
    return (PreprocessDir, ParamDir, logDir, TypLocDir, ConfDir, outputDir)


DELTA = 0.000001


def FloatEqual(a, b):
    return abs(a - b) < DELTA


class Raster:
    def __init__(self, nRows, nCols, data, noDataValue=None, geotransform=None, srs=None):
        self.nRows = nRows
        self.nCols = nCols
        self.data = numpy.copy(data)
        self.noDataValue = noDataValue
        self.geotrans = geotransform
        self.srs = srs

        self.dx = geotransform[1]
        self.xMin = geotransform[0]
        self.xMax = geotransform[0] + nCols * geotransform[1]
        self.yMax = geotransform[3]
        self.yMin = geotransform[3] + nRows * geotransform[5]
        self.validZone = self.data != self.noDataValue
        self.validValues = numpy.where(self.validZone, self.data, numpy.nan)

    def GetAverage(self):
        return numpy.nanmean(self.validValues)

    def GetMax(self):
        return numpy.nanmax(self.validValues)

    def GetMin(self):
        return numpy.nanmin(self.validValues)

    def GetSTD(self):
        return numpy.nanstd(self.validValues)

    def GetSum(self):
        return numpy.nansum(self.validValues)

    def GetValueByRowCol(self, row, col):
        if row < 0 or row >= self.nRows or col < 0 or col >= self.nCols:
            raise ValueError("The row or col must be >=0 and less than nRows or nCols!")
        else:
            value = self.data[int(round(row))][int(round(col))]
            if value == self.noDataValue:
                return None
            else:
                return value

    def GetValueByXY(self, x, y):
        if x < self.xMin or x > self.xMax or y < self.yMin or y > self.yMax:
            raise ValueError("The x or y value must be within the Min and Max!")
        else:
            row = self.nRows - int(numpy.ceil((y - self.yMin) / self.dx))
            col = int(numpy.floor((x - self.xMin) / self.dx))
            value = self.data[row][col]
            if value == self.noDataValue:
                return None
            else:
                return value

def ReadRaster(rasterFile):
    ds = gdal.Open(rasterFile)
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray()
    xsize = band.XSize
    ysize = band.YSize

    noDataValue = band.GetNoDataValue()
    geotrans = ds.GetGeoTransform()

    srs = osr.SpatialReference()
    srs.ImportFromWkt(ds.GetProjection())
    # print srs.ExportToProj4()
    if noDataValue is None:
        noDataValue = NODATA_VALUE
    band = None
    ds = None
    return Raster(ysize, xsize, data, noDataValue, geotrans, srs)


def WriteGTiffFile(filename, nRows, nCols, data, geotransform, srs, noDataValue, gdalType):
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    ds = driver.Create(filename, nCols, nRows, 1, gdalType)
    ds.SetGeoTransform(geotransform)
    ds.SetProjection(srs.ExportToWkt())
    ds.GetRasterBand(1).SetNoDataValue(noDataValue)
    ds.GetRasterBand(1).WriteArray(data)
    ds = None


def WriteAscFile(filename, data, xsize, ysize, geotransform, noDataValue):
    header = """NCOLS %d
NROWS %d
XLLCENTER %f
YLLCENTER %f
CELLSIZE %f
NODATA_VALUE %f
""" % (xsize, ysize, geotransform[0] + 0.5 * geotransform[1], geotransform[3] - (ysize - 0.5) * geotransform[1],
       geotransform[1], noDataValue)

    f = open(filename, 'w')
    f.write(header)
    for i in range(0, ysize):
        for j in range(0, xsize):
            f.write(str(data[i][j]) + "\t")
        f.write("\n")
    f.close()


def Raster2GeoTIFF(tif, geotif, unitConvert = False, zUnitConvert = False, gdalType = gdal.GDT_Float32):
    print "Convering raster's format to GeoTIFF..."
    rstFile = ReadRaster(tif)
    if unitConvert:  # Convert coordinate unit from feet to meter
        converter = 0.3048
        xMin = rstFile.xMin * converter
        dx = rstFile.dx * converter
        yMax = rstFile.yMax * converter
        convertedGeotrans = [xMin, dx, 0, yMax, 0, -dx]
        if zUnitConvert:
            rstFile.data *= converter
        WriteGTiffFile(geotif, rstFile.nRows, rstFile.nCols, rstFile.data, convertedGeotrans, rstFile.srs,
                       rstFile.noDataValue, gdalType)
    else:
        WriteGTiffFile(geotif, rstFile.nRows, rstFile.nCols, rstFile.data, rstFile.geotrans, rstFile.srs,
                       rstFile.noDataValue, gdalType)


def GetRasterStat(rasterFile):
    dataset = gdal.Open(rasterFile, GA_ReadOnly)
    if not dataset is None:
        band = dataset.GetRasterBand(1)
        max = band.GetMaximum()
        min = band.GetMinimum()
        if max is None or min is None:
            (min, max) = band.ComputeRasterMinMax(1)
        mean, std = band.ComputeBandStats()
        band = None
        dataset = None
        return (max, min, mean, std)
    dataset = None


def RPICal(distDown, distUp, RPI):
    down = ReadRaster(distDown)
    up = ReadRaster(distUp)
    temp = down.data < 0
    rpiData = numpy.where(temp, down.noDataValue, down.data / (down.data + up.data))
    WriteGTiffFile(RPI, down.nRows, down.nCols, rpiData, down.geotrans, down.srs, down.noDataValue, gdal.GDT_Float32)


def slopeTrans(tanslp, slp):
    origin = ReadRaster(tanslp)
    temp = origin.data == origin.noDataValue
    slpdata = numpy.where(temp, origin.noDataValue, numpy.arctan(origin.data) * 180. / numpy.pi)
    WriteGTiffFile(slp, origin.nRows, origin.nCols, slpdata, origin.geotrans, origin.srs, origin.noDataValue,
                   gdal.GDT_Float32)


def NegativeDEM(DEM, negDEM):
    origin = ReadRaster(DEM)
    max = numpy.max(origin.data)
    temp = origin.data < 0
    neg = numpy.where(temp, origin.noDataValue, max - origin.data)
    WriteGTiffFile(negDEM, origin.nRows, origin.nCols, neg, origin.geotrans, origin.srs, origin.noDataValue,
                   gdal.GDT_Float32)


def RasterStatistics(rasterFile):
    ds = gdal.Open(rasterFile)
    band = ds.GetRasterBand(1)
    min, max, mean, std = band.ComputeStatistics(False)
    return (min, max, mean, std)


def WriteLog(logfile, contentlist):
    if os.path.exists(logfile):
        logStatus = open(logfile, 'a')
    else:
        logStatus = open(logfile, 'w')
    for content in contentlist:
        logStatus.write("%s\n" % content)
    logStatus.flush()
    logStatus.close()


def WriteTimeLog(logfile, time):
    if os.path.exists(logfile):
        logStatus = open(logfile, 'a')
    else:
        logStatus = open(logfile, 'w')
        logStatus.write("Function Name\tRead Time\tCompute Time\tWrite Time\tTotal Time\t\n")
    logStatus.write(
            "%s\t%s\t%s\t%s\t%s\t\n" % (time['name'], time['readt'], time['computet'], time['writet'], time['totalt']))
    logStatus.flush()
    logStatus.close()


## D8 flow directions in TauDEM, value(DELTA_row, DELTA_col)
DIR_ITEMS = {1: (0, 1),
             2: (-1, 1),
             3: (-1, 0),
             4: (-1, -1),
             5: (0, -1),
             6: (1, -1),
             7: (1, 0),
             8: (1, 1)}
DIR_VALUES = [1, 2, 3, 4, 5, 6, 7, 8]
## corresponding to ArcGIS
## DIR_VALUES = [1,128,64,32,16,8,4,2]
drow = [0, -1, -1, -1, 0, 1, 1, 1]  ## row, not include itself
dcol = [1, 1, 0, -1, -1, -1, 0, 1]  ## col

DIR_PAIRS = [(0, 1),
             (-1, 1),
             (-1, 0),
             (-1, -1),
             (0, -1),
             (1, -1),
             (1, 0),
             (1, 1)]

## find downslope coordinate for D8 and D-inf flow models
def downstream_index(DIR_VALUE, i, j):
    drow, dcol = DIR_ITEMS[DIR_VALUE]
    return i + drow, j + dcol


# D-inf flow model
e = 0
ne = math.pi * 0.25
n = math.pi * 0.5
nw = math.pi * 0.75
w = math.pi
sw = math.pi * 1.25
s = math.pi * 1.5
se = math.pi * 1.75
angleList = [e, ne, n, nw, w, sw, s, se]


def CheckOrtho(a):
    if FloatEqual(a, e):
        return 1
    elif FloatEqual(a, ne):
        return 2
    elif FloatEqual(a, n):
        return 3
    elif FloatEqual(a, nw):
        return 4
    elif FloatEqual(a, w):
        return 5
    elif FloatEqual(a, sw):
        return 6
    elif FloatEqual(a, s):
        return 7
    elif FloatEqual(a, se):
        return 8
    else:
        return 0


def AssignDirCode(a):
    d = CheckOrtho(a)
    if d != 0:
        down = [d]
        return down
    else:
        if a < ne:  ## 129 = 1+128
            down = [1, 2]
        elif a < n:  ## 192 = 128+64
            down = [2, 3]
        elif a < nw:  ## 96 = 64+32
            down = [3, 4]
        elif a < w:  ## 48 = 32+16
            down = [4, 5]
        elif a < sw:  ## 24 = 16+8
            down = [5, 6]
        elif a < s:  ## 12 = 8+4
            down = [6, 7]
        elif a < se:  ## 6 = 4+2
            down = [7, 8]
        else:  ## 3 = 2+1
            down = [8, 1]
        return down


def downstream_index_dinf(dinfDir, i, j):
    downDirs = AssignDirCode(dinfDir)
    # print dinfDir,i,j,downDirs
    downCoors = []
    for dir in downDirs:
        row, col = downstream_index(dir, i, j)
        downCoors.append([row, col])
    return downCoors


## Export ESRI Shapefile -- Line feature
def WriteLineShp(lineList, outShp):
    print ("Write line shapefile: %s" % outShp)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if driver is None:
        print ("ESRI Shapefile driver not available.")
        sys.exit(1)
    if os.path.exists(outShp):
        driver.DeleteDataSource(outShp)
    ds = driver.CreateDataSource(outShp.rpartition(os.sep)[0])
    if ds is None:
        print ("ERROR Output: Creation of output file failed.")
        sys.exit(1)
    lyr = ds.CreateLayer(outShp.rpartition(os.sep)[2].split('.')[0], None, ogr.wkbLineString)
    #    for field in fields:
    #        fieldDefn = ogr.FieldDefn(field,ogr.OFTString)
    #        fieldDefn.SetWidth(255)
    #        lyr.CreateField(fieldDefn)
    for l in lineList:
        #        defn = lyr.GetLayerDefn()
        #        featureFields = ogr.Feature(defn)
        #        for field in fields:
        #            featureFields.SetField(field,"test")
        line = ogr.Geometry(ogr.wkbLineString)
        for i in l:
            line.AddPoint(i[0], i[1])
        templine = ogr.CreateGeometryFromJson(line.ExportToJson())
        feature = ogr.Feature(lyr.GetLayerDefn())
        feature.SetGeometry(templine)
        lyr.CreateFeature(feature)
        feature.Destroy()
    ds.Destroy()


def StringInList(str, strList):
    newStrList = strList[:]
    for i in range(len(newStrList)):
        newStrList[i] = newStrList[i].lower()
    if str.lower() in newStrList:
        return True
    else:
        return


def StripStr(str):
    ### @Function: Remove space(' ') and indent('\t') at the begin and end of the string
    oldStr = ''
    newStr = str
    while oldStr != newStr:
        oldStr = newStr
        newStr = oldStr.strip('\t')
        newStr = newStr.strip(' ')
    return newStr


def SplitStr(str, spliters = None):
    ### @Function: Split string by spliter space(' ') and indent('\t') as default
    # spliters = [' ', '\t']
    # spliters = []
    # if spliter is not None:
    #     spliters.append(spliter)
    if spliters is None:
        spliters = [' ', '\t']
    destStrs = []
    srcStrs = [str]
    while True:
        oldDestStrs = srcStrs[:]
        for s in spliters:
            for srcS in srcStrs:
                tempStrs = srcS.split(s)
                for tempS in tempStrs:
                    tempS = StripStr(tempS)
                    if tempS != '':
                        destStrs.append(tempS)
            srcStrs = destStrs[:]
            destStrs = []
        if oldDestStrs == srcStrs:
            destStrs = srcStrs[:]
            break
    return destStrs


def SplitStr4Float(str, spliters = None):
    strs = SplitStr(str, spliters)
    floats = []
    for str in strs:
        try:
            floats.append(float(str))
        except:
            raise ValueError("The input must be numeric string!")
    return floats


def StringMatch(str1, str2):
    if str1.lower() == str2.lower():
        return True
    else:
        return False


def GetCoreFileName(filepath):
    if isFileExists(filepath):
        return os.path.basename(filepath).split('.')[0]
    else:
        return ''


def FindNumberFromString(s):
    '''
    Find numeric values from string, e.g., 1, .7, 1.2, 4e2, 3e-3, -9, etc.
    reference:
    https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string-in-python/4703508#4703508
    :param s: string which may contains numeric values
    :return: list of numeric values
    '''
    numeric_const_pattern = r'[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?'
    strs = re.findall(numeric_const_pattern, s)
    if len(strs) == 0:
        return None
    else:
        return [float(v) for v in strs]

def GetExecutableFullPath(name):
    '''
    Not for Windows
    get the full path of a given executable name
    :return:
    '''
    process = subprocess.Popen('which %s' % name, shell = True, stdout = subprocess.PIPE)
    findout = process.stdout.readlines()
    if findout == [] or len(findout) == 0:
        print "%s is not included in the env path" % name
        exit(-1)
    return findout[0].split('\n')[0]

## test code ##
if __name__ == '__main__':
    # tanslp = r'C:\Users\ZhuLJ\Desktop\test\DinfSlp.tif'
    # slp = r'C:\Users\ZhuLJ\Desktop\test\Slp.tif'
    # slopeTrans(tanslp, slp)
    s1 = '[[0.99, 1.0], [0.00 , 1.0], [0.0, 1.0]]'
    print FindNumberFromString(s1)
