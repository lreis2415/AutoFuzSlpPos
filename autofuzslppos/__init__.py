# -*- coding: utf-8 -*-
"""
/***************************************************************************
 pyAutoFuzSlpPos
                      Python for Automatic Fuzzy Slope Positions
 Python workflow for data preparation, running model, etc.

 Currently, the following commonly used slope position systems are supported, i.e.,
     - three basic types: ridge, backslope, and valley
     - five basic types: ridge, shoulder slope, backslope, footslope and valley.

 TODO, 11 slope positions considering the concavity and convexity along both
     the contour and profile directions will be considered in the future.

 [1] Qin, C-Z, Zhu, A-X, Shi, X, Li, B-L, Pei, T, and Zhou, C-H. 2009.
        Quantification of spatial gradation of slope positions.
        Geomorphology 110, 152–161.
        doi:10.1016/j.geomorph.2009.04.003

 [2] Zhu, L-J, Zhu, A-X, Qin, C-Z, and Liu, J-Z. 2018.
        Automatic approach to deriving fuzzy slope positions.
        Geomorphology 304, 173-183. doi:10.1016/j.geomorph.2017.12.024

                              -------------------
        author               : Liangjun Zhu, Chengzhi Qin
        copyright            : (C) 2015 - 2019 Lreis, IGSNRR, CAS
        email                : zlj@lreis.ac.cn
 ******************************************************************************
 *                                                                            *
 *   AutoFuzSlpPos is distributed for Research and/or Education only, any     *
 *   commercial purpose will be FORBIDDEN. AutoFuzSlpPos is an open-source    *
 *   project, but without ANY WARRANTY, WITHOUT even the implied warranty of  *
 *   MERCHANTABILITY or FITNESS for A PARTICULAR PURPOSE.                     *
 *   See the GNU General Public License for more details.                     *
 *                                                                            *
 ******************************************************************************/
"""
__author__ = 'Liangjun Zhu'
__email__ = 'zlj@lreis.ac.cn'
__version__ = '1.2.1'
