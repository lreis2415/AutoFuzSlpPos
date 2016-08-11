#! /usr/bin/env python
# coding=utf-8
# @Description: Extract ridge sources for RPI calculation using Skidmore (1990).
#               1. Identify original ridge sources, which are cells that has no cells flow in.
#               2. Using
#               3.
# @Author     : Liang-Jun Zhu
# @Date       : 2016-8-7
#

from Nomenclature import *

sys.setrecursionlimit(10000)
def findRidge(tagValue, num, rdgGRID):
    '''
    find ridge sources using flow direction (D8 or Dinf)
    :param tagValue: value to identify the ridge
    :param rdgGRID: Output ridge source grid
    '''
    if FlowModel:
        flowdir = DinfFlowDir
    else:
        flowdir = D8FlowDir
    direction = ReadRaster(flowdir)
    rows = direction.nRows
    cols = direction.nCols
    direc = direction.data
    # initial ridge source grid
    rdg = numpy.ones((rows, cols)) * tagValue
    for row in range(rows):
        for col in range(cols):
            tempdir = direc[row][col]
            if tempdir == direction.noDataValue:
                rdg[row][col] = NODATA_VALUE
            else:
                if FlowModel:
                    # D-inf flow model
                    tempCoor = downstream_index_dinf(tempdir, row, col)
                    for Coor in tempCoor:
                        temprow, tempcol = Coor
                        if temprow >= 0 and temprow < rows and tempcol >= 0 and tempcol < cols:
                            rdg[temprow][tempcol] = NODATA_VALUE
                else:
                    # D8 flow model
                    temprow, tempcol = downstream_index(tempdir, row, col)
                    if temprow >= 0 and temprow < rows and tempcol >= 0 and tempcol < cols:
                        rdg[temprow][tempcol] = NODATA_VALUE
    WriteGTiffFile(RdgOrgSrc, rows, cols, rdg, direction.geotrans, direction.srs, NODATA_VALUE, gdal.GDT_Float32)

    # read subbasin and indentify the potential ridges
    subbsn = ReadRaster(SubBasin)
    subbsnData = subbsn.data
    subbsn_nodata = subbsn.noDataValue
    potRdg = numpy.ones((rows, cols)) * NODATA_VALUE
    for row in range(rows):
        for col in range(cols):
            if subbsnData[row][col] != subbsn_nodata:
                for i in range(len(dcol)):
                    newRow = row + drow[i]
                    newCol = col + dcol[i]
                    if newRow >= 0 and newRow < rows and newCol >= 0 and newCol < cols:
                        if subbsnData[row][col] != subbsnData[newRow][newCol]:
                            potRdg[row][col] = 1
                            if subbsnData[newRow][newCol] != subbsn_nodata:
                                potRdg[newRow][newCol] = 1
            else:
                potRdg[row][col] = NODATA_VALUE
    WriteGTiffFile(potRdgFromSubbsn, rows, cols, potRdg, direction.geotrans, direction.srs, NODATA_VALUE,
                   gdal.GDT_Float32)
    for row in range(rows):
        for col in range(cols):
            if rdg[row][col] == 1:
                if potRdg[row][col] == NODATA_VALUE:
                    flag = False
                    for i in range(len(dcol)):
                        newRow = row + drow[i]
                        newCol = col + dcol[i]
                        if newRow >= 0 and newRow < rows and newCol >= 0 and newCol < cols:
                            if potRdg[newRow][newCol] != NODATA_VALUE:
                                flag = True
                                break
                    if not flag:
                        rdg[row][col] = NODATA_VALUE
    # eliminate unreasonable ridges based on elevation (mean - 1.39 * STD)
    # read DEM and calculate the mean relative elevation of the original ridge source
    if FlowModel:
        elevR = ReadRaster(DinfDistDown_V)
    else:
        elevR = ReadRaster(D8DistDown_V)
    elevData = elevR.validValues
    # elev_nodata = elevR.noDataValue
    # elevMax = elevR.GetMax()
    # elevMin = elevR.GetMin()
    cond = potRdg != NODATA_VALUE
    validValues = numpy.where(cond, potRdg, numpy.nan)
    validValues = validValues * elevData

    meanElev = numpy.nanmean(validValues)
    stdElev = numpy.nanstd(validValues)
    quantile25 = numpy.nanpercentile(validValues, 25)
    if meanElev < 1.39 * stdElev:
        elevT = meanElev
    else:
        elevT = meanElev - 1.39 * stdElev
    print meanElev, stdElev, elevT, quantile25
    elevT = max(elevT, quantile25)

    vlyR = ReadRaster(VlySrcCal)
    vlysrcData = vlyR.data
    vlysrc_nodata = vlyR.noDataValue
    for row in range(rows):
        for col in range(cols):
            if rdg[row][col] != NODATA_VALUE:
                for i in range(len(dcol)):
                    newRow = row + drow[i]
                    newCol = col + dcol[i]
                    if vlysrcData[newRow][newCol] == D8StreamTag or vlysrcData[row][col] == vlysrc_nodata:
                        rdg[row][col] = NODATA_VALUE
                    if numpy.isnan(elevData[row][col]) or elevData[row][col] < elevT:
                        rdg[row][col] = NODATA_VALUE

    # eliminate ridges with very few continuous cells, e.g., less than 3 cells will be ignored
    for i in range(rows):
        for j in range(cols):
            if rdg[i][j] == 1:
                tempIdx = [[i, j]]
                ContinuousGRID(rdg, i, j, tempIdx, int(num))
                count = len(tempIdx)
                # print count
                if count > 0 and count <= int(num):
                    for rc in tempIdx:
                        rdg[rc[0]][rc[1]] = NODATA_VALUE
    WriteGTiffFile(rdgGRID, rows, cols, rdg, direction.geotrans, direction.srs, NODATA_VALUE, gdal.GDT_Float32)


def ContinuousGRID(numpyArray, row, col, idx, thresh):
    nrows, ncols = numpyArray.shape
    for i in range(len(dcol)):
        newRow = row + drow[i]
        newCol = col + dcol[i]
        if newRow >= 0 and newRow < nrows and newCol >= 0 and newCol < ncols:
            if numpyArray[newRow][newCol] == numpyArray[row][col]:
                if not [newRow, newCol] in idx:
                    idx.append([newRow, newCol])
                    if len(idx) < thresh:
                        ContinuousGRID(numpyArray, newRow, newCol, idx, thresh)


if __name__ == '__main__':
    ini, proc, root = GetInputArgs()
    LoadConfiguration(ini, proc, root)
    findRidge(1, 3, RdgSrcCal)
