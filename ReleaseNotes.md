# AutoFuzSlpPos-Releases notes

+ 2024-10-24: Build Docker image based on taudem_ext:debian.

+ 2019-01-23: The C++ programs of AutoFuzSlpPos have been integrated into [TauDEM_ext](https://github.com/lreis2415/TauDEM_ext).
  + add TauDEM_ext as subtree
    ```shell
    git remote add -f taudem_ext git@github.com:lreis2415/TauDEM_ext.git -m master
    git subtree add --prefix=autofuzslppos/taudem_ext taudem_ext master --squash
    ```
  + pull from TauDEM_ext
    ```shell
    git fetch taudem_ext master
    git subtree pull --prefix=autofuzslppos/taudem_ext taudem_ext master --squash
    ```
   + push changes to TauDEM_ext
    ```shell
    git subtree push --prefix=autofuzslppos/taudem_ext taudem_ext master
    ```
+ 2017-12-20:
  + Using PyGeoC as 3rdparty libarary.
  + Update TauDEM from 5.1.2 to 5.3.7. Use [TauDEM_ext](https://github.com/lreis2415/TauDEM_ext) as subtree.
  + Add auto configured test script (`test/run_demo_data_bydefault.py`) with demo data.
+ 2017-8-1: Refactor the entire python workflow based on pylint and Google style. In the meanwhile, releae the main page of AutoFuzSlpPos: http://lreis2415.github.io/AutoFuzSlpPos/
+ 2017-7-18: Compiled binaries

  From now on, each release will be attached the compiled binaries under selected environments automatically by [Travis CI](https://travis-ci.org/lreis2415/AutoFuzSlpPos) and [Appveyor](https://ci.appveyor.com/project/lreis-2415/autofuzslppos).

  + Windows-MSVC 2013-32/64bit with MSMPI-v8
  + Linux(Ubuntu trusty)-GCC-4.8 with MPICH2-3.0.4

  This release can be used for Geomorphology Manuscript.


+ 2017-1-16: Release for Geomorphology Manuscript

  This release is coupled with the manuscript for Geomorphology.

  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.831377.svg)](https://doi.org/10.5281/zenodo.831377)

  Related identifiers:
​	Supplement to: https://github.com/lreis2415/AutoFuzSlpPos/tree/v2017.1.16
