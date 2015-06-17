AutoFuzSlpPos (short for "Automated Extraction of Fuzzy Slope Position") is developed by PhD candidate Liangjun Zhu and Prof. Chengzhi Qin.
Contact and support email: zlj@lreis.ac.cn
AutoFuzSlpPos is designed to extract fuzzy slope position information in hillslope scale based on the method proposed by Qin et al.(2009) and Qin et al.(2012).
[Qin, C.Z., Zhu, A.X., Shi, X., Li, B.L., Pei, T., Zhou, C.H., 2009. Quantification of spatial gradation of slope positions. Geomorphology 110, 152-161.
Qin, C.-Z., Zhu, A.-X., Qiu, W.-L., Lu, Y.-J., Li, B.-L., Pei, T., 2012. Mapping soil organic matter in small low-relief catchments using fuzzy slope position information. Geoderma 171, 64-74.]

AutoFuzSlpPos is based on TauDEM parallelized framework and submitted to TauDEM LICENSE. Several functions of TauDEM are used to accomplish the preprocessing from DEM, include   Pitremove, D8FlowDir, DinfFlowDir, AreaD8, Threshold, MoveOutletsToStreams, AreaDinf, DinfDistDown.
Also, some functions revised from TauDEM are developed, include D8DistDownToStream, D8DistUpToRidge, DinfDistUpToRidge.
Besides, new functions are designed, include Curvature, SelectTypLocSlpPos, FuzzySlpPosInference and HardenSlpPos.

AutoFuzSlpPos is programmed using C++ and Python. It can be compiled by Microsoft Visual Studio on Windows and GCC 4.7+ compiler on Linux/Unix. We have tested on Windows 7, CentOS 6.2 and Ubuntu 14.04. 

1. INSTALLATION
	1.1 Compile with CMAKE and nmake (Visual Studio) on Windows Platform
	1) Check the MPI Library path in line 7~9 in CMakeLists.txt to make sure they are correct for your environment.
	2) From Start menu, run "Visual Studio Command Prompt (2010)" as administrator.
	3) cd Destination_Build_Path, for example C:\AutoFuzSlpPos\build
	4) cmake Source_Path, for example C:\AutoFuzSlpPos\src, this will generate Visual Studio Project file. Then you can edit or compile through VS.
	5) instead of step 4), We recommend this method to compile executable files.
		cmake -G "NMake Makefiles" Source_Path
		nmake
	
	1.2 Compile with makefile on Linux/Unix Platform
	1) compile MPICH, reference http://www.mpich.org/downloads/
	2) cd to the src folder, check the MPI_DIR in line 33 in makefile to make sure it is correct for you.
	3) make. By default, the executable file will be located in ../exec_linux_x86. You can change INSTALLDIR to control it.
	
	Then, you are ready to run the program through py_main/AutoFuzSlpPos_main.py
2. 