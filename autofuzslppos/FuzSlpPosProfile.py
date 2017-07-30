#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract fuzzy slope positions along flow path from ridge to valley.
    1. Identify ridge sources, by default, ridge means there are no cells flow in.
    2. Trace down and extract the similarities of fuzzy slope positons.
    3. Construct the output ESRI Shapefile.
    @author   : Liangjun Zhu
    @changelog: 15-09-08  lj - initial implementation
                17-07-30  lj - reorganize and incorporate with pygeoc
"""
from autofuzslppos.Config import get_input_cfgs
# from Nomenclature import *
# from Util import *


def fuzSlpPosProfile(rdgCoors, d8flowdir, d8stream, shpfile):
    '''
    extract fuzzy slope positions and other attributes along flow path
    :param rdgCoors:  the coordinates of ridge, such as [[3,4],[9,8]]  format: [row,col]
    :param d8flowdir: used to trace downslope
    :param d8stream: used to determining termination of each flow path
    :param shpfile: results ESRI Shapefile
    '''
    direction = ReadRaster(d8flowdir)
    rows = direction.nRows
    cols = direction.nCols
    direc = direction.data
    geo = direction.geotrans
    nodata = direction.noDataValue
    stream = ReadRaster(d8stream).data
    streamNodata = ReadRaster(d8stream).noDataValue
    profileCoorList = []  ## store xy coordinate
    profileList = []  ## store row and col
    cellsizeList = []  ## 1 or 1.414
    count = 0
    preLength = 0
    for rdgCoor in rdgCoors:
        tempPath = []
        tempPathCoor = []
        tempCellsize = []
        row, col = rdgCoor
        while (stream[row][col] != 1 or stream[row][col] == streamNodata) and \
                        row >= 2 and row < rows - 2 and col >= 2 and col < cols - 2:
            tempPath.append([row, col])
            tempPathCoor.append([geo[0] + (col + 0.5) * geo[1], geo[3] - (row + 0.5) * geo[1]])
            tempdir = direc[row][col]
            if tempdir in [1, 3, 5, 7]:
                tempCellsize.append(1)
            else:
                tempCellsize.append(1.414)
            if tempdir != nodata:
                row, col = downstream_index(tempdir, row, col)
        tempPath.append([row, col])
        tempPathCoor.append([geo[0] + (col + 0.5) * geo[1], geo[3] - (row + 0.5) * geo[1]])

        curLength = len(tempPath)
        if curLength > 20:
            profileCoorList.append(tempPathCoor)
            cellsizeList.append(tempCellsize)
        count += 1
        # preLength = curLength
        print count, curLength
        # profileList.append(tempPath)
        # profileCoorList.append(tempPathCoor)
        # print tempPath
    # fieldNames = ["count","cellsize","elev","rdg","shd","bks","fts","vly","maxsimi","harden"]
    WriteLineShp(profileCoorList, shpfile)


def main():
    """TEST CODE"""
    fuzslppos_cfg = get_input_cfgs()
    # ini, proc, root = get_input_args()
    # LoadConfiguration(ini, proc, root)
    ## input data
    ## Flowdir: D8FlowDir or DinfFlowDir, DEM: demfil, etc...
    ## output file: rdg_taudem, ProfileFuzSlpPos
    ## step 1
    # print DinfFlowDir
    # rdgsrcCoors = ReadRidge()
    # print rdgsrcInpug
    ## step 2
    # attrList = [demfil, RdgInf, ShdInf, BksInf, FtsInf, VlyInf, MaxSimilarity, HardenSlpPos]
    # fuzSlpPosProfile(rdgsrcCoors, D8FlowDir, D8Stream, ProfileFuzSlpPos)


if __name__ == '__main__':
    main()
