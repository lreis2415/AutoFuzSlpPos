# -*- coding: utf-8 -*-
"""Delineate subbasins and hillslopes based on TauDEM functions with PyGeoC.

    @author: Liangjun Zhu (zlj@lreis.ac.cn)
    @date  : 2020-03-28
"""

from __future__ import absolute_import, unicode_literals

import os
import argparse

from pygeoc.TauDEM import TauDEMFilesUtils, TauDEMWorkflow
from pygeoc.hydro import Hillslopes

from pygeoc.utils import FileClass, UtilClass


class ParseArguments(object):
    def __init__(self, in_dem='', in_wp='', in_cores=2, in_outlet=None, in_thresh=0,
                 in_singlebasin=False, in_streamvalue=-1):
        self.dem = in_dem
        self.wp = in_wp
        self.predir = ''
        self.resultdir = ''
        self.n = in_cores
        self.outlet = in_outlet
        self.threshold = in_thresh
        self.singlebasin = in_singlebasin
        self.streamvalue = in_streamvalue

        self.stream = ''
        self.fd8 = ''
        self.hs = ''

    def check(self):
        if self.dem == '' or self.dem is None:
            print('The input DEM cannot be empty!')
            return False
        if not os.path.exists(self.dem):
            print('The input DEM (%s) does not exist!' % self.dem)
            return False
        if self.wp != '' and self.wp is not None:
            UtilClass.mkdir(self.wp)
        else:
            core_name = FileClass.get_core_name_without_suffix(self.dem)
            self.wp = os.path.dirname(self.dem) + os.sep + 'workspace_' + core_name
        self.predir = self.wp + os.sep + 'PreDir'
        self.resultdir = self.wp + os.sep + 'Hillslope'
        UtilClass.mkdir(self.predir)
        UtilClass.mkdir(self.resultdir)

        if self.n is None:
            self.n = 2

        if self.outlet != '' and self.outlet is not None:
            if not os.path.exists(self.outlet):
                print('The input outlet (%s) file does not exist!' % self.outlet)
                self.outlet = None
        else:
            self.outlet = None

        if self.threshold is None or self.threshold < 0:
            self.threshold = 0
        else:
            print('Input threshold: %s' % repr(self.threshold))

        if self.streamvalue is None or not -1 <= self.streamvalue <= 4:
            self.streamvalue = -1
        else:
            self.streamvalue = int(self.streamvalue)
            print('Input streamvalue: %s' % repr(self.threshold))

        namecfg = TauDEMFilesUtils(self.predir)
        self.stream = namecfg.stream_raster
        self.fd8 = namecfg.d8flow

        self.hs = '%s/hillslope.tif' % self.resultdir

        return True


def get_arguments(desc='Automatic workflow to delineate hillslopes based on TauDEM and PyGeoC.'):
    """Parse arguments.
    """
    # define input arguments
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-dem', type=str, help='Full path of DEM file', required=True)
    parser.add_argument('-wp', type=str, help='Full path of workspace', required=False)
    parser.add_argument('-n', type=int, help='Number of cores used for parallel computing',
                        required=False)
    parser.add_argument('-outlet', type=str, help='Full path of watershed outlet (.shp)',
                        required=False)
    parser.add_argument('-thresh', type=float, help='Threshold for extracting streams',
                        required=False)
    parser.add_argument('-streamvalue', type=int,
                        help='Method for handling stream value in hillslope raster',
                        required=False)

    # add mutually group
    psa_group = parser.add_mutually_exclusive_group()
    psa_group.add_argument('-singlebasin', action='store_true',
                           help='The input DEM belongs to one single watershed or not',
                           required=False)
    # psa_group.add_argument('-preprocess', action='store_true', help='Run preprocess or not',
    #                        required=False)
    # psa_group.add_argument('-subbasin', action='store_true', help='Delineate subbasin or not',
    #                        required=False)
    # parse arguments
    args = parser.parse_args()
    arguments_obj = ParseArguments(in_dem=args.dem, in_wp=args.wp, in_cores=args.n,
                                   in_outlet=args.outlet, in_thresh=args.thresh,
                                   in_singlebasin=args.singlebasin,
                                   in_streamvalue=args.streamvalue)
    if not arguments_obj.check():
        return None
    return arguments_obj


def main():
    """Main entrance."""
    args_obj = get_arguments()
    if args_obj is None:
        return

    TauDEMWorkflow.watershed_delineation(args_obj.n, args_obj.dem,
                                         outlet_file=args_obj.outlet,
                                         thresh=args_obj.threshold,
                                         singlebasin=args_obj.singlebasin,
                                         workingdir=args_obj.predir,
                                         avoid_redo=True)

    Hillslopes.downstream_method_whitebox(args_obj.stream, args_obj.fd8, args_obj.hs,
                                          stream_value_method=args_obj.streamvalue)


if __name__ == "__main__":
    main()
