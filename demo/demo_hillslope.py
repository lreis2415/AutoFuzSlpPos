# -*- coding: utf-8 -*-
"""Run demo data of Jamaica.

    @revisions:
      1. 2024-10-28 - lj - Support the ini configuration file as input

    @author: Liangjun Zhu (zlj@lreis.ac.cn)
    @date: 2021-10-25
"""
from __future__ import absolute_import, unicode_literals

import os
import sys

if os.path.abspath(os.path.join(sys.path[0], '..')) not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(sys.path[0], '..')))

from pygeoc.utils import UtilClass
from pygeoc.TauDEM import TauDEMWorkflow
from pygeoc.hydro import Hillslopes

from autofuzslppos.Config import AutoFuzSlpPosConfig, check_input_args, get_input_cfgs
from hillslope_delineation import ParseArguments


def main():
    """Main workflow."""
    ini_file, bin_dir, input_proc, rawdem, root_dir = get_input_cfgs()
    if ini_file is None and bin_dir is None and input_proc < 0 and rawdem is None and root_dir is None:
        cur_path = UtilClass.current_path(lambda: 0)
        bin_dir = os.path.abspath(os.path.join(cur_path, '../build/bin'))
        demo_data_path = os.path.abspath(os.path.join(cur_path, '../data/Jamaica'))
        # print(demo_data_path)
        dem_name = 'Jamaica_dem'
        workspace = demo_data_path + os.sep + 'workspace_hillslope_%s' % dem_name
        UtilClass.mkdir(workspace)
        dem_path = demo_data_path + os.sep + dem_name + '.tif'
    else:
        cfg = AutoFuzSlpPosConfig(*check_input_args(ini_file, bin_dir, input_proc, rawdem, root_dir))
        bin_dir = cfg.bin_dir
        workspace = cfg.ws
        dem_path = cfg.dem

    args_obj = ParseArguments(in_dem=dem_path, in_wp=workspace)
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
