# -*- coding: utf-8 -*-
"""Extract fuzzy slope positions along flow path from ridge to valley.

    - 1. Read ridge sources, by default, ridge means there are no cells flow in.
    - 2. Trace down and extract the similarities of fuzzy slope positions.
    - 3. Construct the output ESRI Shapefile.

    @author   : Liangjun Zhu

    @changelog:
    - 2020-01-10  lj - initial implementation.
"""
from __future__ import absolute_import, unicode_literals
import os
import sys

if os.path.abspath(os.path.join(sys.path[0], '..')) not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(sys.path[0], '..')))

from pygeoc.raster import RasterUtilClass
from pygeoc.hydro import D8Util
from pygeoc.vector import VectorUtilClass

from autofuzslppos.Config import get_input_cfgs


def read_ridge_sources(rdgfile):
    """Read ridge sources from raster file and return coordinates lists
    """
    rdgsrcr = RasterUtilClass.read_raster(rdgfile)
    rows = rdgsrcr.nRows
    cols = rdgsrcr.nCols
    rdgsrcd = rdgsrcr.data
    nodata = rdgsrcr.noDataValue
    rdgCoors = list()
    for row in range(rows):
        for col in range(cols):
            if rdgsrcd[row][col] != 0 and rdgsrcd[row][col] != nodata:
                rdgCoors.append([row, col])
    return rdgCoors


def trace_downslope_paths(rdgcoors, d8fdfile, streamfile):
    """Trace down according to D8 flow direction and return profile lists.

    The profile coordinates follows the format:

    {rdgCellID: {'profileCoors': [[100, 20], [100, 21], ...]}
    """
    directionr = RasterUtilClass.read_raster(d8fdfile)
    rows = directionr.nRows
    cols = directionr.nCols
    direc = directionr.data
    geo = directionr.geotrans
    nodata = directionr.noDataValue
    streamr = RasterUtilClass.read_raster(streamfile)
    stream = streamr.data
    stream_nodata = streamr.noDataValue

    def rowcol_to_geocoor(crow, ccol):
        return [geo[0] + (ccol + 0.5) * geo[1], geo[3] - (crow + 0.5) * geo[1]]

    flowpaths = list()
    pathlengths = list()
    for i, rdgcoor in enumerate(rdgcoors):
        tempPathCoor = list()
        tempPathLength = list()
        row, col = rdgcoor
        tempPathCoor.append(rowcol_to_geocoor(row, col))
        pathLength = 0
        tempPathLength.append(pathLength)
        while (stream[row][col] <= 0 or stream[row][col] == stream_nodata) \
            and 2 <= row < rows - 2 and 2 <= col < cols - 2 and direc[row][col] != nodata:
            tempdir = int(direc[row][col])  # default D8 flow direction and TauDEM-coding
            if tempdir in [1, 3, 5, 7]:
                pathLength += directionr.dx
            else:
                pathLength += directionr.dx * 1.4142135623730951
            tempPathLength.append(pathLength)
            row, col = D8Util.downstream_index(tempdir, row, col)
            tempPathCoor.append(rowcol_to_geocoor(row, col))

        flowpaths.append(tempPathCoor)
        pathlengths.append(tempPathLength)
    return flowpaths, pathlengths


def read_attributes_along_flowpaths(flowpaths, pathlens, attrslist, profileattrcsv):
    """Read attributes from raster layers for each point along flow paths
    """
    # The basic structure is:
    # {rdgCellID: {'profileCoors': [[100, 20], [100, 21], ...],
    #              'attributes': {'attr1': [223, 220, ...],
    #                             'attr2': [0.99, 0.89, ...],
    #                             }
    #             }
    # }
    profile_attr_dict = dict()
    profile_attr_dict['fields'] = ['x', 'y', 'length']
    attrdata = list()
    for attrname, attrfile in list(attrslist.items()):
        profile_attr_dict['fields'].append(attrname)
        attrdata.append(RasterUtilClass.read_raster(attrfile))
    for idx, (paths, lens) in enumerate(list(zip(flowpaths, pathlens))):
        profile_attr_dict[idx] = list()
        for (curx, cury), curlen in list(zip(paths, lens)):
            curitem = [curx, cury, curlen]
            for adata in attrdata:
                curitem.append(adata.get_value_by_xy(curx, cury))
            profile_attr_dict[idx].append(curitem)

    # write out
    log_status = open(profileattrcsv, 'w', encoding='utf-8')
    log_status.write('ID,%s\n' % ','.join(profile_attr_dict['fields']))
    for idx, contentlist in list(profile_attr_dict.items()):
        if idx == 'fields':
            continue
        for content in contentlist:
            log_status.write('%d,%s\n' % (idx, ','.join('%.4f' % i for i in content)))
    log_status.flush()
    log_status.close()


def main():
    """TEST CODE"""
    fuzslppos_cfg = get_input_cfgs()

    profileAttrCsv = fuzslppos_cfg.ws.pre_dir + os.sep + 'profiles_attributes_bothtyploc.csv'
    profileShp = fuzslppos_cfg.ws.pre_dir + os.sep + 'profiles_bothtyploc.shp'

    # rdgCoors = read_ridge_sources(fuzslppos_cfg.pretaudem.rdgsrc)  # ridge source by dinf
    firsttyp = fuzslppos_cfg.slppostype[0]
    rdgCoors = read_ridge_sources(fuzslppos_cfg.singleslpposconf[firsttyp].typloc)  # ridge typloc
    # dstRaster = fuzslppos_cfg.pretaudem.stream_raster  # valley source defined by stream
    dstRaster = fuzslppos_cfg.singleslpposconf[fuzslppos_cfg.slppostype[-1]].typloc  # valley typloc
    flowPaths, pathLengths = trace_downslope_paths(rdgCoors, fuzslppos_cfg.pretaudem.d8flow,
                                                   dstRaster)

    attrsList = {'dem': fuzslppos_cfg.pretaudem.filldem}
    for typ in fuzslppos_cfg.slppostype:
        attrsList[typ] = fuzslppos_cfg.singleslpposconf[typ].fuzslppos
    read_attributes_along_flowpaths(flowPaths, pathLengths, attrsList, profileAttrCsv)

    VectorUtilClass.write_line_shp(flowPaths, profileShp)


if __name__ == '__main__':
    main()
