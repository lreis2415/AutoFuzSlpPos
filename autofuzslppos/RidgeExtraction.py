#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract ridge sources using flow direction, subbasin, and elevation.

    1. Identify original ridge sources (RdgOrgSrc), which are cells that have no flow-in cells
       or have very few flow-in proportion for Dinf (TODO).\n
    2. Read subbasin and identify the boundary grids as potential ridges (RdgPotSrc).\n
    3. Sort each subbasin's boundary cells by elevation, filter by the a given percent, e.g. 70%.\n
    4. Filter RdgOrgSrc by RdgPotSrc.

    Be caution, the derived ridge sources may need manually modification when further use.

    @author   : Liangjun Zhu

    @changelog: 16-08-07  lj - initial implementation.\n
                17-08-09  lj - reorganize and incorporate with pygeoc.\n
"""
import os

import numpy

from autofuzslppos.Config import get_input_cfgs
from autofuzslppos.pygeoc.pygeoc.hydro.hydro import FlowModelConst
from autofuzslppos.pygeoc.pygeoc.hydro.postTauDEM import D8Util, DinfUtil
from autofuzslppos.pygeoc.pygeoc.raster.raster import RasterUtilClass
from autofuzslppos.pygeoc.pygeoc.utils.utils import MathClass, FileClass, DEFAULT_NODATA


# sys.setrecursionlimit(10000)
#
#
# def recursive_continuous_cells(numpyarray, row, col, idx):
#     nrows, ncols = numpyarray.shape
#     for r, c in DIR_PAIRS:
#         new_row = row + r
#         new_col = col + c
#         if 0 <= new_row < nrows and 0 <= new_col < ncols:
#             if numpyarray[new_row][new_col] == numpyarray[row][col]:
#                 if not [new_row, new_col] in idx:
#                     idx.append([new_row, new_col])
#                     recursive_continuous_cells(numpyarray, new_row, new_col, idx)
#
#
# def findRidge(tagValue, rdgGRID):
#     '''
#     find ridge sources using flow direction (D8 or Dinf)
#     :param tagValue: value to identify the ridge
#     :param rdgGRID: Output ridge source grid
#     '''
#     if FlowModel:
#         flowdir = DinfFlowDir
#     else:
#         flowdir = D8FlowDir
#     direction = ReadRaster(flowdir)
#     rows = direction.nRows
#     cols = direction.nCols
#     direc = direction.data
#     # initial ridge source grid
#     t1 = time.time()
#     rdg = numpy.ones((rows, cols)) * tagValue
#
#     WriteGTiffFile(RdgOrgSrc, rows, cols, rdg, direction.geotrans, direction.srs, NODATA_VALUE,
#                    gdal.GDT_Float32)
#     # print ("initial ridges time: %f" % (time.time() - t1))
#
#     # eliminate unreasonable ridges based on elevation
#     # read DEM and calculate the mean relative elevation of the original ridge source
#     t1 = time.time()
#     if FlowModel:
#         elevR = ReadRaster(DinfDistDown_V)
#     else:
#         elevR = ReadRaster(D8DistDown_V)
#     elevData = elevR.validValues
#     # elev_nodata = elevR.noDataValue
#     # elevMax = elevR.GetMax()
#     # elevMin = elevR.GetMin()
#     #    Method 1: Use the relative elevation of the boundary of subbasins
#     # cond = potRdg != NODATA_VALUE
#     # validValues = numpy.where(cond, potRdg, numpy.nan)
#     #    Method 2: Use the relative elevation of the ridge sources to determine the elevation threshold
#     cond = rdg != NODATA_VALUE
#     validValues = numpy.where(cond, rdg, numpy.nan)
#     validValues = validValues * elevData
#     meanElev = numpy.nanmean(validValues)
#     stdElev = numpy.nanstd(validValues)
#     quantile25 = numpy.nanpercentile(validValues, 25)
#     if meanElev < stdElev:
#         elevT = meanElev
#     else:
#         elevT = meanElev - stdElev
#     # print (meanElev, stdElev, elevT, quantile25)
#
#     elevT = max(elevT, quantile25)
#
#     # Filter by elevation threshold
#     t1 = time.time()
#     for row in range(rows):
#         for col in range(cols):
#             if rdg[row][col] == NODATA_VALUE or numpy.isnan(elevData[row][col]) or \
#                             elevData[row][col] < elevT:
#                 rdg[row][col] = NODATA_VALUE
#     # print ("elevation threshold time: %f" % (time.time() - t1))
#     WriteGTiffFile(RdgOrgSrc, rows, cols, rdg, direction.geotrans, direction.srs, NODATA_VALUE,
#                    gdal.GDT_Float32)
#     # read subbasin and identify the potential ridges
#     t1 = time.time()
#     subbsn = ReadRaster(SubBasin)
#     subbsnData = subbsn.data
#     subbsn_nodata = subbsn.noDataValue
#     potRdg = numpy.ones((rows, cols)) * NODATA_VALUE
#     for row in range(rows):
#         for col in range(cols):
#             if subbsnData[row][col] != subbsn_nodata:
#                 for r, c in DIR_PAIRS:
#                     newRow = row + r
#                     newCol = col + c
#                     if 0 <= newRow < rows and 0 <= newCol < cols:
#                         if subbsnData[row][col] != subbsnData[newRow][newCol]:
#                             potRdg[row][col] = 1
#                             if subbsnData[newRow][newCol] != subbsn_nodata:
#                                 potRdg[newRow][newCol] = 1
#             else:
#                 potRdg[row][col] = NODATA_VALUE
#     WriteGTiffFile(potRdgFromSubbsn, rows, cols, potRdg, direction.geotrans, direction.srs,
#                    NODATA_VALUE,
#                    gdal.GDT_Float32)
#     count = 0
#     for row in range(rows):
#         for col in range(cols):
#             if rdg[row][col] == 1:
#                 if potRdg[row][col] == NODATA_VALUE:
#                     flag = False
#                     for r, c in DIR_PAIRS:
#                         newRow = row + r
#                         newCol = col + c
#                         if 0 <= newRow < rows and 0 <= newCol < cols:
#                             if potRdg[newRow][newCol] != NODATA_VALUE:
#                                 flag = True
#                                 break
#                     if not flag:
#                         rdg[row][col] = NODATA_VALUE
#                         count += 1
#     # print ("total %d ridge are excluded according to subbasin boundary." % count)
#     # print ("identify ridge from subbasin time: %f" % (time.time() - t1))
#
#     # If coincident with valley source, then delete. This step may not be necessary. Deprecated!
#     # count = 0
#     # vlyR = ReadRaster(VlySrcCal)
#     # vlysrcData = vlyR.data
#     # vlysrc_nodata = vlyR.noDataValue
#     # for row in range(rows):
#     #     for col in range(cols):
#     #         if rdg[row][col] != NODATA_VALUE:
#     #             for r, c in DIR_PAIRS:
#     #                 newRow = row + r
#     #                 newCol = col + c
#     #                 if vlysrcData[newRow][newCol] == D8StreamTag or vlysrcData[row][col] == vlysrc_nodata:
#     #                     rdg[row][col] = NODATA_VALUE
#     #                     count += 1
#     # print ("total %d ridge are excluded according to valley sources." % count)
#     # print ("valley exclude time: %f" % (time.time() - t1))
#
#     # eliminate ridges with very few continuous cells, e.g., less than 3 cells will be ignored.
#     # this procedure should not be happened, since the single cell may be the typical location. Deprecated!
#     # t1 = time.time()
#     # for i in range(rows):
#     #     for j in range(cols):
#     #         if rdg[i][j] == 1:
#     #             tempIdx = [[i, j]]
#     #             recursive_continuous_cells(rdg, i, j, tempIdx)
#     #             count = len(tempIdx)
#     #             # print count
#     #             for tmpR, tmpC in tempIdx:
#     #                 rdg[tmpR][tmpC] = count
#     #             # if count > 0 and count <= int(num):
#     #             #     for rc in tempIdx:
#     #             #         rdg[rc[0]][rc[1]] = NODATA_VALUE
#     # print ("continuous Grid time: %f" % (time.time() - t1))
#
#     WriteGTiffFile(rdgGRID, rows, cols, rdg, direction.geotrans, direction.srs, NODATA_VALUE,
#                    gdal.GDT_Float32)
#

class RidgeSourceExtraction(object):
    """Class for extracting ridge sources."""

    def __init__(self, flowdirf, subbsnf, elevf, rdgsrc, flow_model=1, prop=0., ws=None):
        """Initialize file names."""
        FileClass.check_file_exists(flowdirf)
        FileClass.check_file_exists(subbsnf)
        FileClass.check_file_exists(elevf)
        if ws is None:
            ws = os.path.basename(flowdirf)
        self.ws = ws
        if flow_model == 1:
            suffix = '_dinf.tif'
        else:
            suffix = '_d8.tif'
        self.rdgorg = self.ws + os.sep + 'RdgOrgSrc' + suffix
        self.boundsrc = self.ws + os.sep + 'RdgPotSrc' + suffix
        self.boundsrcfilter = self.ws + os.sep + 'RdgPotSrcFilter' + suffix

        if rdgsrc is None:
            rdgsrc = self.ws + os.sep + 'rdgsrc' + suffix
        self.rdgsrc = rdgsrc
        self.flowmodel = flow_model
        self.prop = prop
        # read raster data
        flowdir_r = RasterUtilClass.read_raster(flowdirf)
        self.flowdir_data = flowdir_r.data
        self.nrows = flowdir_r.nRows
        self.ncols = flowdir_r.nCols
        self.nodata_flow = flowdir_r.noDataValue
        self.geotrans = flowdir_r.geotrans
        self.srs = flowdir_r.srs
        subbsn_r = RasterUtilClass.read_raster(subbsnf)
        self.subbsn_data = subbsn_r.data
        self.nodata_subbsn = subbsn_r.noDataValue
        elev_r = RasterUtilClass.read_raster(elevf)
        self.elev_data = elev_r.data
        self.nodata_elev = elev_r.noDataValue

        # initialize output arrays
        self.rdgsrc_data = numpy.ones((self.nrows, self.ncols)) * 1
        self.rdgpot = numpy.ones((self.nrows, self.ncols)) * DEFAULT_NODATA

    def ridge_without_flowin_cell(self):
        """Find the original ridge sources that have no flow-in cells."""
        for row in range(self.nrows):
            for col in range(self.ncols):
                tempdir = self.flowdir_data[row][col]
                if MathClass.floatequal(tempdir, self.nodata_flow):
                    self.rdgsrc_data[row][col] = DEFAULT_NODATA
                    continue
                if self.flowmodel == 1:  # Dinf flow model
                    temp_coor = DinfUtil.downstream_index_dinf(tempdir, row, col)
                    for temprow, tempcol in temp_coor:
                        if 0 <= temprow < self.nrows and 0 <= tempcol < self.ncols:
                            self.rdgsrc_data[temprow][tempcol] = DEFAULT_NODATA
                        else:
                            self.rdgsrc_data[row][col] = DEFAULT_NODATA
                else:  # D8 flow model
                    temprow, tempcol = D8Util.downstream_index(tempdir, row, col)
                    if 0 <= temprow < self.nrows and 0 <= tempcol < self.ncols:
                        self.rdgsrc_data[temprow][tempcol] = DEFAULT_NODATA
                    else:
                        self.rdgsrc_data[row][col] = DEFAULT_NODATA
        RasterUtilClass.write_gtiff_file(self.rdgorg, self.nrows, self.ncols, self.rdgsrc_data,
                                         self.geotrans, self.srs, DEFAULT_NODATA, 6)

    def subbasin_boundary_cells(self, subbsn_perc):
        """Subbasin boundary cells that are potential ridge sources."""
        dir_deltas = FlowModelConst.d8delta_ag.values()
        subbsn_elevs = dict()

        def add_elev_to_subbsn_elevs(sid, elev):
            if sid not in subbsn_elevs:
                subbsn_elevs[sid] = [elev]
            else:
                subbsn_elevs[sid].append(elev)

        for row in range(self.nrows):
            for col in range(self.ncols):
                if MathClass.floatequal(self.subbsn_data[row][col], self.nodata_subbsn):
                    continue
                for r, c in dir_deltas:
                    new_row = row + r
                    new_col = col + c
                    if 0 <= new_row < self.nrows and 0 <= new_col < self.ncols:
                        if MathClass.floatequal(self.subbsn_data[new_row][new_col],
                                                self.nodata_subbsn):
                            subbsnid = self.subbsn_data[row][col]
                            self.rdgpot[row][col] = subbsnid
                            add_elev_to_subbsn_elevs(subbsnid, self.elev_data[row][col])
                        elif not MathClass.floatequal(self.subbsn_data[row][col],
                                                      self.subbsn_data[new_row][new_col]):
                            subbsnid = self.subbsn_data[row][col]
                            subbsnid2 = self.subbsn_data[new_row][new_col]
                            self.rdgpot[row][col] = subbsnid
                            self.rdgpot[new_row][new_col] = subbsnid2
                            add_elev_to_subbsn_elevs(subbsnid, self.elev_data[row][col])
                            add_elev_to_subbsn_elevs(subbsnid2, self.elev_data[new_row][new_col])

        RasterUtilClass.write_gtiff_file(self.boundsrc, self.nrows, self.ncols, self.rdgpot,
                                         self.geotrans, self.srs, DEFAULT_NODATA, 6)
        subbsn_elevs_thresh = dict()
        for sid, elevs in subbsn_elevs.iteritems():
            tmpelev = numpy.array(elevs)
            tmpelev.sort()
            subbsn_elevs_thresh[sid] = tmpelev[int(len(tmpelev) * subbsn_perc)]
        for row in range(self.nrows):
            for col in range(self.ncols):
                if MathClass.floatequal(self.rdgpot[row][col], DEFAULT_NODATA):
                    continue
                if self.elev_data[row][col] < subbsn_elevs_thresh[self.subbsn_data[row][col]]:
                    self.rdgpot[row][col] = DEFAULT_NODATA
        RasterUtilClass.write_gtiff_file(self.boundsrcfilter, self.nrows, self.ncols, self.rdgpot,
                                         self.geotrans, self.srs, DEFAULT_NODATA, 6)

    def run(self):
        """Entrance."""
        self.ridge_without_flowin_cell()
        self.subbasin_boundary_cells(0.5)


def main():
    """Main workflow."""
    cfg = get_input_cfgs()
    flowmodel = cfg.flow_model
    if flowmodel == 1:
        flowdir = cfg.pretaudem.dinf
    else:
        flowdir = cfg.pretaudem.d8flow
    subbasin = cfg.pretaudem.subbsn
    elev = cfg.pretaudem.filldem
    prop = 0.
    ws = cfg.ws.pre_dir
    rdg = cfg.ridge

    rdgsrc_obj = RidgeSourceExtraction(flowdir, subbasin, elev, rdg, flowmodel, prop, ws)
    rdgsrc_obj.run()


if __name__ == '__main__':
    main()
