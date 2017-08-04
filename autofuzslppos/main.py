#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Prototype-based fuzzy slope positions.

    @author   : Liangjun Zhu

    @changelog: 15-03-20  lj - initial implementation.\n
                17-07-30  lj - reorganize and incorporate with pygeoc.
"""

from autofuzslppos.Config import get_input_cfgs
from autofuzslppos.FuzzySlpPosInference import fuzzy_inference
from autofuzslppos.PreProcessing import pre_processing
from autofuzslppos.SelectTypLoc import extract_typical_location


def main():
    """Main workflow."""
    fuzslppos_cfg = get_input_cfgs()

    pre_processing(fuzslppos_cfg)
    extract_typical_location(fuzslppos_cfg)
    fuzzy_inference(fuzslppos_cfg)


if __name__ == '__main__':
    main()
