#! /usr/bin/env python
#coding=utf-8

from Util import Raster2GeoTIFF
import TauDEM
## TIFFConvert
## Convert other grid format to GeoTIFF
## Any Grid format supported by GDAL is permitted
## Invoke format: Raster2GeoTIFF(rawdem, dem, flag=False)
##                when flag is True, then convert feet to meter.
rawdem = r'E:\data_m\AutoFuzSlpPos\C&G_zhu_2016\CompareWithQin2009\basinBased\profc_basin.tif'
dem  = r'E:\data_m\AutoFuzSlpPos\C&G_zhu_2016\CompareWithQin2009\basinBased\Params\ProfC.tif'
Raster2GeoTIFF(rawdem, dem)