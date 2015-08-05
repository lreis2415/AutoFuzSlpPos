#! /usr/bin/env python
#coding=utf-8

from Util import *
import TauDEM
rawdem = r'E:\research\fuzzyslppos\AutoFuzSlpPos\PV_Dinf_1m\dem1m.tif'
dem  = r'E:\research\fuzzyslppos\AutoFuzSlpPos\PV_Dinf_1m\dem1meter.tif'
TIFF2GeoTIFF(rawdem, dem)