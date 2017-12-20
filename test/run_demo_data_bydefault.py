#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Run demo data by default settings.

    @author   : Liangjun Zhu
"""
import os
import sys

if os.path.abspath(os.path.join(sys.path[0], '..')) not in sys.path:
    sys.path.append(os.path.abspath(os.path.join(sys.path[0], '..')))

try:
    from ConfigParser import ConfigParser  # py2
except ImportError:
    from configparser import ConfigParser  # py3

from pygeoc.utils import UtilClass

from autofuzslppos.Config import AutoFuzSlpPosConfig
from autofuzslppos.FuzzySlpPosInference import fuzzy_inference
from autofuzslppos.PreProcessing import pre_processing
from autofuzslppos.SelectTypLoc import extract_typical_location


def write_autofuzslppos_config_file(ini_name, bin, wp, data_path, dem_name):
    UtilClass.mkdir(wp)
    org_ini_file = data_path + os.sep + ini_name
    demf = data_path + os.sep + 'inputs' + os.sep + dem_name
    if not os.path.isfile(org_ini_file):
        print ('%s file is not existed!' % org_ini_file)
        exit(-1)
    dst_int_file = wp + os.sep + ini_name

    cfg_items = list()
    with open(org_ini_file, 'r') as f:
        for line in f.readlines():
            cfg_items.append(line.strip())
    # print cfg_items
    cfg_items.append('[REQUIRED]')
    cfg_items.append('exeDir = %s' % bin)
    cfg_items.append('rootDir = %s' % wp)
    cfg_items.append('rawdem = %s' % demf)

    with open(dst_int_file, 'w') as f:
        for item in cfg_items:
            f.write(item + '\n')

    cf = ConfigParser()
    cf.read(dst_int_file)
    return AutoFuzSlpPosConfig(cf)


def main():
    """Main workflow."""
    cur_path = UtilClass.current_path()
    print cur_path
    workspace = cur_path + os.sep + 'workspace'
    bin_dir = os.path.abspath(os.path.join(cur_path, '../bin'))
    print bin_dir
    demo_data_path = os.path.abspath(os.path.join(cur_path, '../data/demo_data'))
    print demo_data_path
    org_ini_name = 'Jamaica_demo.ini'
    dem_name = 'Jamaica_dem.tif'

    fuzslppos_cfg = write_autofuzslppos_config_file(org_ini_name, bin_dir,
                                                    workspace, demo_data_path,
                                                    dem_name)

    pre_processing(fuzslppos_cfg)
    extract_typical_location(fuzslppos_cfg)
    fuzzy_inference(fuzslppos_cfg)


if __name__ == '__main__':
    main()
