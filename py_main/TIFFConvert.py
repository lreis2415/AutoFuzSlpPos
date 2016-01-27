#! /usr/bin/env python
#coding=utf-8

from Util import TIFF2GeoTIFF
import TauDEM
## TIFFConvert
## Convert other grid format to GeoTIFF
## Any Grid format supported by GDAL is permitted
## Invoke format: TIFF2GeoTIFF(rawdem, dem, flag=False)
##                when flag is True, then convert feet to meter.
rawdem = r'E:\research\Digital_terrain_analysis\autoFuzSlpPos\data\PleasantValley\pv-elev-meterFil.asc'
dem  = r'E:\research\Digital_terrain_analysis\autoFuzSlpPos\data\PleasantValley\pv-elev-meter.tif'
TIFF2GeoTIFF(rawdem, dem)