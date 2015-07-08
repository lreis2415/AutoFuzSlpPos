#! /usr/bin/env python
#coding=utf-8

from Util import *
import TauDEM
rawdem = r'E:\github-zlj\AutoFuzSlpPos\data\PleasantValley\pvdem.tif'
dem  = r'E:\github-zlj\AutoFuzSlpPos\data\PleasantValley\dem.tif'
TIFF2GeoTIFF(rawdem, dem)