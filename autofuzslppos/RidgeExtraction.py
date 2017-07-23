#! /usr/bin/env python
# coding=utf-8
# @Description: Extract ridge sources for original RPI calculation using Skidmore (1990).
#               1. Identify original ridge sources (RdgOrgSrc), which are cells that have no flow-in cells.
#                  which is the most time-consuming step.
#               2. Read subbasin and identify the boundary grids as potential ridges (RdgPotSrc)
#               3. Filter RdgOrgSrc by RdgPotSrc.
#               4. Filter by a given or default elevation threshold.
# @Author     : Liang-Jun Zhu
# @Date       : 2016-8-7
#
#
import time
from Nomenclature import *

sys.setrecursionlimit(10000)


def recursive_continuous_cells(numpyarray, row, col, idx):
    nrows, ncols = numpyarray.shape
    for r, c in DIR_PAIRS:
        new_row = row + r
        new_col = col + c
        if 0 <= new_row < nrows and 0 <= new_col < ncols:
            if numpyarray[new_row][new_col] == numpyarray[row][col]:
                if not [new_row, new_col] in idx:
                    idx.append([new_row, new_col])
                    recursive_continuous_cells(numpyarray, new_row, new_col, idx)


def findRidge(tagValue, rdgGRID):
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
    t1 = time.time()
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
                    for temprow, tempcol in tempCoor:
                        if 0 <= temprow < rows and 0 <= tempcol < cols:
                            rdg[temprow][tempcol] = NODATA_VALUE
                        else:
                            rdg[row][col] = NODATA_VALUE
                else:
                    # D8 flow model
                    temprow, tempcol = downstream_index(tempdir, row, col)
                    if 0 <= temprow < rows and 0 <= tempcol < cols:
                        rdg[temprow][tempcol] = NODATA_VALUE
                    else:
                        rdg[row][col] = NODATA_VALUE
    WriteGTiffFile(RdgOrgSrc, rows, cols, rdg, direction.geotrans, direction.srs, NODATA_VALUE, gdal.GDT_Float32)
    # print ("initial ridges time: %f" % (time.time() - t1))

    # eliminate unreasonable ridges based on elevation
    # read DEM and calculate the mean relative elevation of the original ridge source
    t1 = time.time()
    if FlowModel:
        elevR = ReadRaster(DinfDistDown_V)
    else:
        elevR = ReadRaster(D8DistDown_V)
    elevData = elevR.validValues
    # elev_nodata = elevR.noDataValue
    # elevMax = elevR.GetMax()
    # elevMin = elevR.GetMin()
    #    Method 1: Use the relative elevation of the boundary of subbasins
    # cond = potRdg != NODATA_VALUE
    # validValues = numpy.where(cond, potRdg, numpy.nan)
    #    Method 2: Use the relative elevation of the ridge sources to determine the elevation threshold
    cond = rdg != NODATA_VALUE
    validValues = numpy.where(cond, rdg, numpy.nan)
    validValues = validValues * elevData
    meanElev = numpy.nanmean(validValues)
    stdElev = numpy.nanstd(validValues)
    quantile25 = numpy.nanpercentile(validValues, 25)
    if meanElev < stdElev:
        elevT = meanElev
    else:
        elevT = meanElev - stdElev
    # print (meanElev, stdElev, elevT, quantile25)

    elevT = max(elevT, quantile25)

    # Filter by elevation threshold
    t1 = time.time()
    for row in range(rows):
        for col in range(cols):
            if rdg[row][col] == NODATA_VALUE or numpy.isnan(elevData[row][col]) or\
                            elevData[row][col] < elevT:
                rdg[row][col] = NODATA_VALUE
    # print ("elevation threshold time: %f" % (time.time() - t1))
    WriteGTiffFile(RdgOrgSrc, rows, cols, rdg, direction.geotrans, direction.srs, NODATA_VALUE, gdal.GDT_Float32)
    # read subbasin and identify the potential ridges
    t1 = time.time()
    subbsn = ReadRaster(SubBasin)
    subbsnData = subbsn.data
    subbsn_nodata = subbsn.noDataValue
    potRdg = numpy.ones((rows, cols)) * NODATA_VALUE
    for row in range(rows):
        for col in range(cols):
            if subbsnData[row][col] != subbsn_nodata:
                for r, c in DIR_PAIRS:
                    newRow = row + r
                    newCol = col + c
                    if 0 <= newRow < rows and 0 <= newCol < cols:
                        if subbsnData[row][col] != subbsnData[newRow][newCol]:
                            potRdg[row][col] = 1
                            if subbsnData[newRow][newCol] != subbsn_nodata:
                                potRdg[newRow][newCol] = 1
            else:
                potRdg[row][col] = NODATA_VALUE
    WriteGTiffFile(potRdgFromSubbsn, rows, cols, potRdg, direction.geotrans, direction.srs, NODATA_VALUE,
                   gdal.GDT_Float32)
    count = 0
    for row in range(rows):
        for col in range(cols):
            if rdg[row][col] == 1:
                if potRdg[row][col] == NODATA_VALUE:
                    flag = False
                    for r, c in DIR_PAIRS:
                        newRow = row + r
                        newCol = col + c
                        if 0 <= newRow < rows and 0 <= newCol < cols:
                            if potRdg[newRow][newCol] != NODATA_VALUE:
                                flag = True
                                break
                    if not flag:
                        rdg[row][col] = NODATA_VALUE
                        count += 1
    # print ("total %d ridge are excluded according to subbasin boundary." % count)
    # print ("identify ridge from subbasin time: %f" % (time.time() - t1))

    # If coincident with valley source, then delete. This step may not be necessary. Deprecated!
    # count = 0
    # vlyR = ReadRaster(VlySrcCal)
    # vlysrcData = vlyR.data
    # vlysrc_nodata = vlyR.noDataValue
    # for row in range(rows):
    #     for col in range(cols):
    #         if rdg[row][col] != NODATA_VALUE:
    #             for r, c in DIR_PAIRS:
    #                 newRow = row + r
    #                 newCol = col + c
    #                 if vlysrcData[newRow][newCol] == D8StreamTag or vlysrcData[row][col] == vlysrc_nodata:
    #                     rdg[row][col] = NODATA_VALUE
    #                     count += 1
    # print ("total %d ridge are excluded according to valley sources." % count)
    # print ("valley exclude time: %f" % (time.time() - t1))

    # eliminate ridges with very few continuous cells, e.g., less than 3 cells will be ignored.
    # this procedure should not be happened, since the single cell may be the typical location. Deprecated!
    # t1 = time.time()
    # for i in range(rows):
    #     for j in range(cols):
    #         if rdg[i][j] == 1:
    #             tempIdx = [[i, j]]
    #             recursive_continuous_cells(rdg, i, j, tempIdx)
    #             count = len(tempIdx)
    #             # print count
    #             for tmpR, tmpC in tempIdx:
    #                 rdg[tmpR][tmpC] = count
    #             # if count > 0 and count <= int(num):
    #             #     for rc in tempIdx:
    #             #         rdg[rc[0]][rc[1]] = NODATA_VALUE
    # print ("continuous Grid time: %f" % (time.time() - t1))

    WriteGTiffFile(rdgGRID, rows, cols, rdg, direction.geotrans, direction.srs, NODATA_VALUE, gdal.GDT_Float32)


if __name__ == '__main__':
    import time
    t1 = time.time()
    ini, proc, root = get_input_args()
    LoadConfiguration(ini, proc, root)
    findRidge(1, RdgSrcCal)
    print ("execute time: %f" % (time.time() - t1))