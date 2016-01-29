#! /usr/bin/env python
#coding=utf-8
## Extract fuzzy slope positions along flow path from ridge to valley.
## Prepared by Liangjun Zhu, 2015-08-09
## 1. Identify ridge sources, ridge means there are no cells flow in.
## 2. Trace down and extract the similarities of fuzzy slope positons.
## 3. Construct the output ESRI Shapefile.
from Config import *
from Nomenclature import *
from Util import *
import numpy
from osgeo import gdalconst
from gdalconst import *

## find ridge sources, flag can be 0 and 1, 0 means D8 flow model, while
## 1 means D-inf flow model.
def findRidge(flag,flowdir, rdgGRID):
    direction = ReadRaster(flowdir)
    rows = direction.nRows
    cols = direction.nCols
    direc = direction.data
    rdg = numpy.ones((rows,cols))
    for row in range(rows):
        for col in range(cols):
            tempdir = direc[row][col]
            if tempdir == direction.noDataValue:
                rdg[row][col] = direction.noDataValue
            else:
                if flag == 0:
                    ## D8 flow model
                    temprow, tempcol = downstream_index(tempdir, row, col)
                    if temprow >= 0 and temprow < rows and tempcol >= 0 and tempcol < cols:
                        rdg[temprow][tempcol] = 0
                else:
                    ## D-inf flow model
                    tempCoor = downstream_index_dinf(tempdir, row, col)
                    for Coor in tempCoor:
                        temprow, tempcol = Coor
                        if temprow >= 0 and temprow < rows and tempcol >= 0 and tempcol < cols:
                            rdg[temprow][tempcol] = 0
    rdgCoor = []
    for row in range(rows):
        for col in range(cols):
            if rdg[row][col] == 1:
                rdgCoor.append([row,col])
    WriteGTiffFile(rdgGRID, rows, cols, rdg, direction.geotrans, direction.srs, direction.noDataValue, gdal.GDT_Int16)
    return rdgCoor

## extract fuzzy slope positions and other attributes along flow path
## rdgCoors is the coordinates of ridge, such as [[3,4],[9,8]]  format: [row,col]
## d8flowdir is used to trace downslope, d8stream is used to determining termination
## shpfile is the results ESRI Shapefile
def fuzSlpPosProfile(rdgCoors, d8flowdir, d8stream, shpfile):
    direction = ReadRaster(d8flowdir)
    rows = direction.nRows
    cols = direction.nCols
    direc = direction.data
    geo = direction.geotrans
    nodata = direction.noDataValue
    stream = ReadRaster(d8stream).data
    streamNodata = ReadRaster(d8stream).noDataValue
    profileCoorList = [] ## store xy coordinate
    profileList = [] ## store row and col
    cellsizeList = [] ## 1 or 1.414
    count = 0
    preLength = 0
    for rdgCoor in rdgCoors:
        tempPath = []
        tempPathCoor = []
        tempCellsize = []
        row, col = rdgCoor
        while (stream[row][col] != 1 or stream[row][col] == streamNodata) and row >= 2 and row < rows-2 and col >= 2 and col < cols-2:
            tempPath.append([row,col])
            tempPathCoor.append([geo[0] + (col + 0.5) * geo[1], geo[3]-(row+0.5)*geo[1]])
            tempdir = direc[row][col]
            if tempdir in [1,3,5,7]:
                tempCellsize.append(1)
            else:
                tempCellsize.append(1.414)
            if tempdir != nodata:
                row, col = downstream_index(tempdir, row, col)
        tempPath.append([row,col])
        tempPathCoor.append([geo[0] + (col + 0.5) * geo[1], geo[3]-(row+0.5)*geo[1]])

        curLength = len(tempPath)
        if curLength > 20:
            profileCoorList.append(tempPathCoor)
            cellsizeList.append(tempCellsize)
        count = count + 1
        preLength = curLength
        print count,curLength
        #profileList.append(tempPath)
        #profileCoorList.append(tempPathCoor)
        #print tempPath
    #fieldNames = ["count","cellsize","elev","rdg","shd","bks","fts","vly","maxsimi","harden"]
    WriteLineShp(profileCoorList,shpfile)
if __name__ == '__main__':
    ## input data
    ## Flowdir: D8FlowDir or DinfFlowDir, DEM: demfil, etc...
    ## output file: rdg_taudem, ProfileFuzSlpPos
    ## step 1
    #print DinfFlowDir
    rdgsrc = findRidge(1,DinfFlowDir, rdg_taudem)
    #print rdgsrc
    ## step 2
    #attrList = [demfil, RdgInf, ShdInf, BksInf, FtsInf, VlyInf, MaxSimilarity, HardenSlpPos]
    fuzSlpPosProfile(rdgsrc, D8FlowDir, D8Stream, ProfileFuzSlpPos)
    