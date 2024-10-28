# -*- coding: utf-8 -*-
"""Run demo data of Jamaica for comparison of multiple flow direction algorithms.

    @revisions:
      1. 2024-10-28 - lj - Support the ini configuration file as input

    @author: Liangjun Zhu (zlj@lreis.ac.cn)
    @date: 2022-03-08
"""
from __future__ import absolute_import, unicode_literals

import os
import sys

if os.path.abspath(os.path.join(sys.path[0], '..')) not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(sys.path[0], '..')))

from pygeoc.utils import UtilClass
from pygeoc.TauDEM import TauDEM, TauDEM_Ext, TauDEMFilesUtils
from pygeoc.postTauDEM import D8Util, DinfUtil

from autofuzslppos.Config import AutoFuzSlpPosConfig, check_input_args, get_input_cfgs


class TauDEMExtFiles(TauDEMFilesUtils):
    """predefined TauDEM_Ext resulted file names"""
    _DIRCODEMFDMD = 'dirCodeMFDmd.tif'
    _FLOWFRACTIONMFDMD = 'fractionsMFDmd.tif'

    def __init__(self, tau_dir):
        """assign taudem resulted file path"""
        TauDEMFilesUtils.__init__(self, tau_dir)

        self.mfdmd_dir = self.workspace + os.sep + self._DIRCODEMFDMD
        self.mfdmd_frac = self.workspace + os.sep + self._FLOWFRACTIONMFDMD

        result_dir = self.workspace + os.sep + 'FlowDirections'
        UtilClass.rmmkdir(result_dir)
        self.d8flow_esri = result_dir + os.sep + 'd8dir_esri.tif'
        self.dinfflow_esri = result_dir + os.sep + 'dinfdir_esri.tif'
        self.dinfweight_upd = self.workspace + os.sep + 'dinfweight_upd.tif'
        self.dinfang_upd = self.workspace + os.sep + 'dinfang_upd.tif'
        self.mfdmdflow_esri = result_dir + os.sep + 'mfddir_esri.tif'


def main():
    """Main workflow."""
    ini_file, bin_dir, input_proc, rawdem, root_dir = get_input_cfgs()
    if ini_file is None and bin_dir is None and input_proc < 0 and rawdem is None and root_dir is None:
        cur_path = UtilClass.current_path(lambda: 0)
        bin_dir = os.path.abspath(os.path.join(cur_path, '../build/bin'))
        demo_data_path = os.path.abspath(os.path.join(cur_path, '../data/Jamaica'))
        # print(demo_data_path)
        dem_name = 'Jamaica_dem'
        workspace = demo_data_path + os.sep + 'workspace_flowdir_comp_%s' % dem_name
        UtilClass.rmmkdir(workspace)
        dem_path = demo_data_path + os.sep + dem_name + '.tif'
        print(dem_path)
        np = 2
    else:
        cfg = AutoFuzSlpPosConfig(*check_input_args(ini_file, bin_dir, input_proc, rawdem, root_dir))
        bin_dir = cfg.bin_dir
        workspace = cfg.ws.pre_dir
        dem_path = cfg.dem
        np = cfg.proc
    min_frac = 0.0001

    nc = TauDEMExtFiles(workspace)

    # pitremove
    TauDEM.pitremove(np, dem_path, nc.filldem, workspace, None, bin_dir)

    # D8
    TauDEM.d8flowdir(np, nc.filldem, nc.d8flow, nc.slp, workspace, None, bin_dir)
    # Convert D8 encoding rule to ArcGIS
    D8Util.convert_code(nc.d8flow, nc.d8flow_esri)

    # Dinf
    TauDEM.dinfflowdir(np, nc.filldem, nc.dinf, nc.dinf_slp, workspace, None, bin_dir)
    # Convert Dinf to compressed flow direction according to ArcGIS encoding rule
    DinfUtil.output_compressed_dinf(nc.dinf, nc.dinfflow_esri, nc.dinfweight_upd,
                                    minfraction=min_frac,
                                    upddinffile=nc.dinfang_upd)

    # MFD-md
    TauDEM_Ext.mfdmdflowdir(np, nc.filldem, nc.mfdmdflow_esri, nc.mfdmd_frac,
                            min_portion=min_frac,
                            p0=1.1, rng=8.9, lb=0., ub=1.,
                            workingdir=workspace, exedir=bin_dir)


if __name__ == '__main__':
    main()
