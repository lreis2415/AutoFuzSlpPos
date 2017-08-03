#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Utility Classes and Functions
    @author   : Liangjun Zhu
    @changelog: 15-07-31  lj - initial implementation
                17-07-21  lj - reorganize and incorporate with pygeoc
"""

import os

import numpy

from autofuzslppos.pygeoc.pygeoc.raster.raster import RasterUtilClass


def rpi_calculation(distdown, distup, rpi_outfile):
    """Calculate Relative Position Index (RPI)."""
    down = RasterUtilClass.read_raster(distdown)
    up = RasterUtilClass.read_raster(distup)
    temp = down.data < 0
    rpi_data = numpy.where(temp, down.noDataValue, down.data / (down.data + up.data))
    RasterUtilClass.write_gtiff_file(rpi_outfile, down.nRows, down.nCols, rpi_data, down.geotrans,
                                     down.srs, down.noDataValue, down.dataType)


def slope_rad_to_deg(tanslp, slp):
    """Convert slope from radius to slope."""
    origin = RasterUtilClass.read_raster(tanslp)
    temp = origin.data == origin.noDataValue
    slpdata = numpy.where(temp, origin.noDataValue, numpy.arctan(origin.data) * 180. / numpy.pi)
    RasterUtilClass.write_gtiff_file(slp, origin.nRows, origin.nCols, slpdata, origin.geotrans,
                                     origin.srs, origin.noDataValue, origin.dataType)


def write_log(logfile, contentlist):
    if os.path.exists(logfile):
        log_status = open(logfile, 'a')
    else:
        log_status = open(logfile, 'w')
    for content in contentlist:
        log_status.write("%s\n" % content)
    log_status.flush()
    log_status.close()


def write_time_log(logfile, time):
    if os.path.exists(logfile):
        log_status = open(logfile, 'a')
    else:
        log_status = open(logfile, 'w')
        log_status.write("Function Name\tRead Time\tCompute Time\tWrite Time\tTotal Time\t\n")
    log_status.write("%s\t%s\t%s\t%s\t%s\t\n" % (time['name'], time['readt'], time['computet'],
                                                 time['writet'], time['totalt']))
    log_status.flush()
    log_status.close()


def main():
    """TEST CODE"""
    pass


if __name__ == '__main__':
    main()
