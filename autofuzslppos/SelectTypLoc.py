#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Prepare configuration files for selecting typical location.

    @author   : Liangjun Zhu

    @changelog: 15-09-08  lj - initial implementation.\n
                17-07-30  lj - reorganize and incorporate with pygeoc.\n
"""
import os
import time

from pygeoc.utils import StringClass

from Config import get_input_cfgs
from ParasComb import combine_ext_conf_parameters
from TauDEMExtension import TauDEMExtension


def extract_typical_location(cfg):
    """Prepare configuration files for extracting typical location."""
    if not cfg.flag_selecttyploc:
        return 0
    start_t = time.time()
    for i, slppos in enumerate(cfg.slppostype):
        if cfg.flag_auto_typlocparams:  # automatically extract typical location
            # write extract ranges to initial configuration file
            cur_ext_conf = cfg.singleslpposconf[slppos].extinitial
            extconfig_info = open(cur_ext_conf, 'w')
            extconfig_info.write('ProtoTag\t%d\n' % cfg.slppostag[i])
            abandon = list()  # abandoned terrain attributes (full file path)
            for vname, inf in cfg.infshape[slppos].iteritems():
                if StringClass.string_match(inf, 'N'):
                    abandon.append(vname)
            # print abandon
            param_num = 0
            for param in cfg.selectedtopo:
                if param not in abandon:
                    param_num += 1
            extconfig_info.write('ParametersNUM\t%d\n' % param_num)
            for vname, vpath in cfg.selectedtopo.iteritems():
                if vname in abandon:
                    continue
                if vname in cfg.extractrange[slppos] and vname not in abandon:
                    vrange = cfg.extractrange[slppos][vname]
                    extconfig_info.write('Parameters\t%s\t%s\t%f\t%f\n' %
                                         (vname, vpath, vrange[0], vrange[1]))
                else:
                    extconfig_info.write('Parameters\t%s\t%s\t%f\t%f\n' %
                                         (vname, vpath, 0, 0))
            extconfig_info.write('OUTPUT\t%s\n' % cfg.singleslpposconf[slppos].typloc)
            for vname, inf in cfg.infshape[slppos].iteritems():
                if not StringClass.string_match(inf, 'N'):
                    extconfig_info.write('FuzInfShp\t%s\t%s\n' % (vname, inf))
            base_input_param = 'BaseInput\t'
            base_input_param += '\t'.join(str(p) for p in cfg.param4typloc[slppos])
            extconfig_info.write(base_input_param)
            extconfig_info.close()
        else:
            # read from existed extconfig file
            cur_ext_conf = cfg.singleslpposconf[slppos].extconfig
            if not os.path.exists(cur_ext_conf) and len(cfg.extractrange[slppos]) <= 1:
                raise RuntimeError('The input extract config file %s MUST existed when the '
                                   'value ranges setting are absent in *.ini!' % cur_ext_conf)
            else:
                with open(cur_ext_conf, 'r') as extconfig_info:
                    infos = extconfig_info.readlines()
                for line in infos:
                    splitstring = StringClass.split_string(line.split('\n')[0], '\t')
                    if StringClass.string_match(splitstring[0], 'Parameters') \
                            and len(splitstring) == 5 \
                            and splitstring[2] not in cfg.extractrange[slppos]:
                        cfg.extractrange[slppos][splitstring[2]] = [float(splitstring[3]),
                                                                    float(splitstring[4])]
                # rewrite extconfig file
                extconfig_info = open(cur_ext_conf, 'w')
                extconfig_info.write('ProtoTag\t%d\n' % cfg.slppostag[i])
                param_num = len(cfg.extractrange[slppos])
                extconfig_info.write('ParametersNUM\t%d\n' % param_num)
                for vname, vrange in cfg.extractrange[slppos].iteritems():
                    extconfig_info.write('Parameters\t%s\t%s\t%f\t%f\n' %
                                         (vname, cfg.selectedtopo[vname], vrange[0], vrange[1]))
                extconfig_info.write('OUTPUT\t%s\n' % cfg.singleslpposconf[slppos].typloc)
                extconfig_info.close()

        TauDEMExtension.selecttyplocslppos(cfg.proc, cur_ext_conf,
                                           cfg.singleslpposconf[slppos].infrecommend,
                                           cfg.singleslpposconf[slppos].extlog,
                                           cfg.ws.typloc_dir,cfg.mpi_dir, cfg.bin_dir,
                                           cfg.log.all, cfg.hostfile)
    print ('Typical Locations extracted done!')
    # Combine extraction parameters.
    combine_ext_conf_parameters(cfg.slppostype, cfg.singleslpposconf, cfg.slpposresult.extconfig)
    end_t = time.time()
    cost = (end_t - start_t) / 60.
    logf = open(cfg.log.runtime, 'a')
    logf.write('Selection of Typical Locations Time-consuming: ' + str(cost) + ' s\n')
    logf.close()
    return cost


def main():
    """TEST CODE"""
    fuzslppos_cfg = get_input_cfgs()
    extract_typical_location(fuzslppos_cfg)


if __name__ == '__main__':
    main()
