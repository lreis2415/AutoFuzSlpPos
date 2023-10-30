# -*- coding: utf-8 -*-
"""Run demo data of Jamaica.

    @author: Liangjun Zhu (zlj@lreis.ac.cn)
    @date: 2021-10-25
"""
from __future__ import absolute_import, unicode_literals

import os
import sys
if os.path.abspath(os.path.join(sys.path[0], '..')) not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(sys.path[0], '..')))

from pygeoc.utils import UtilClass
from hillslope_delineation import parse_arguments

from pygeoc.TauDEM import TauDEMWorkflow
from pygeoc.hydro import Hillslopes


def main():
    """Main workflow."""
    cur_path = UtilClass.current_path(lambda: 0)
    bin_dir = os.path.abspath(os.path.join(cur_path, '../build/bin'))
    demo_data_path = os.path.abspath(os.path.join(cur_path, '../data/Jamaica'))
    # print(demo_data_path)
    dem_name = 'Jamaica_dem'
    workspace = demo_data_path + os.sep + 'workspace_hillslope_%s' % dem_name
    UtilClass.mkdir(workspace)
    dem_path = demo_data_path + os.sep + dem_name + '.tif'

    args_obj = parse_arguments(in_dem=dem_path, in_wp=workspace)
    if not args_obj.check():
        return

    TauDEMWorkflow.watershed_delineation(args_obj.n, args_obj.dem,
                                         bin_dir=bin_dir,
                                         outlet_file=args_obj.outlet,
                                         thresh=args_obj.threshold,
                                         singlebasin=args_obj.singlebasin,
                                         workingdir=args_obj.predir,
                                         avoid_redo=True)

    Hillslopes.downstream_method_whitebox(args_obj.stream, args_obj.fd8, args_obj.hs,
                                          stream_value_method=args_obj.streamvalue)


if __name__ == '__main__':
    main()
