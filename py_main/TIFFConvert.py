#! /usr/bin/env python
#coding=utf-8

from Util import *
import TauDEM
## TIFFConvert
## Convert other grid format to GeoTIFF
## Any Grid format supported by GDAL is permitted
rawdem = r'E:\data\DEMs\pvdem.asc'
dem  = r'E:\test\test.tif'
TIFF2GeoTIFF(rawdem, dem)