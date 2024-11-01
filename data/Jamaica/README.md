Dear all,

This is a small study area for testing AutoFuzSlpPos. The DEM data can be freely download from http://www.jamaicancaves.org/jamaica-dem.htm.
Data in this directory is organized as follows:

```
-|data
---|README.md
---|Jamaica_demo.ini: Configuration file for directly use with docker.
---|Jamaica_dem.tif: The DEM of the study area as the only input file
---|Jamaica_contour10.shp: The contour shapefile for visualization.
---|workspace_fuzslppos_Jamaica_dem: Automated derived results after running demo/demo_fuzslppos.py
-----|FuzzySlpPos: Fuzzy slope position raster files.
-----|TypLoc: Typical locations (i.e., prototypes) of each slope position.
-----|Params: Automated derived topographic attribute from DEM.
-----|Config: Automated determined parameters for typical locations extraction and fuzzy inference.
-----|DinfpreDir: Preprocessing results, e.g., ridge sources and valley sources.
-----|Log: Log files including runtime information, etc.
```

Note: RDG: ridge; SHD: shoulder slope; BKS: backslope; FTS: footslope; VLY: valley.

For more detailed information, please refer to the submitted manuscript and the
[GitHub homepage](https://github.com/lreis2415/AutoFuzSlpPos).
