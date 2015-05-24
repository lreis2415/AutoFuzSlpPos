#  This file used for make on the CSDMS system
#
cmake_minimum_required(VERSION 2.6)
project(AutoFuzSlpPos)
set (BUILD_SHARED_LIBS OFF)
SET (CMAKE_BUILD_TYPE "Release")
include_directories("C:/Program Files/Microsoft HPC Pack 2012/Inc")
link_directories("C:/Program Files/Microsoft HPC Pack 2012/Lib/i386")
link_libraries("C:/Program Files/Microsoft HPC Pack 2012/Lib/i386/msmpi.lib")

set (shape_srcs
	shapelib/shapefil.h
	shapelib/dbfopen.c
	shapelib/safileio.c
	shapelib/shpopen.c
	shapelib/shptree.c
	ReadOutlets.cpp)


#OBJFILES includes classes, structures, and constants common to all files
set (common_srcs commonLib.cpp tiffIO.cpp)

set (D8FILES aread8mn.cpp aread8.cpp ${common_srcs} ${shape_srcs})
set (DINFFILES areadinfmn.cpp areadinf.cpp ${common_srcs} ${shape_srcs})
set (D8 D8FlowDirmn.cpp d8.cpp Node.cpp ${common_srcs} ${shape_srcs})
set (D8DISTDOWN D8DistDownToStream.cpp D8DistDownToStreammn.cpp ${common_srcs})
set (DINFDISTDOWN DinfDistDown.cpp DinfDistDownmn.cpp ${common_srcs})
set (DINFDISTUP DinfDistUpToRidge.cpp DinfDistUpToRidgemn.cpp ${common_srcs})
set (DINF DinfFlowDirmn.cpp dinf.cpp Node.cpp ${common_srcs} ${shape_srcs})
set (DROPANALYSISFILES DropAnalysis.cpp DropAnalysismn.cpp ${common_srcs} ${shape_srcs})
set (MVOUTLETSTOSTRMFILES moveoutletstostrm.cpp moveoutletstostrmmn.cpp
     ${common_srcs} ${shape_srcs})
set (PITREMOVE flood.cpp PitRemovemn.cpp ${common_srcs})
set (THRESHOLD Threshold.cpp Thresholdmn.cpp ${common_srcs})
#Added by Liangjun Zhu, 2015/5/21
set (CURVATURE Curvature.cpp Curvaturemn.cpp ${common_srcs})
set (D8DISTUP D8DistUpToRidge.cpp D8DistUpToRidgemn.cpp ${common_srcs})
set (FUZSLPPOSINF FuzzySlpPosInference.cpp FuzzySlpPosInferencemn.cpp ${common_srcs})
set (HARDENSLPPOS HardenSlpPos.cpp HardenSlpPosmn.cpp ${common_srcs})
set (TYPLOCSEL stats.cpp SelectTypLocSlpPos.cpp SelectTypLocSlpPosmn.cpp ${common_srcs})
set (CALCULATOR SimpleCalculator.cpp SimpleCalculatormn.cpp ${common_srcs})


add_executable (aread8 ${D8FILES})
add_executable (areadinf ${DINFFILES})
add_executable (d8flowdir ${D8})
add_executable (d8distdowntostream ${D8DISTDOWN})
add_executable (dinfdistdown ${DINFDISTDOWN})
add_executable (dinfdistuptoridge ${DINFDISTUP})
add_executable (dinfflowdir ${DINF})
add_executable (dropanalysis ${DROPANALYSISFILES})
add_executable (moveoutletstostreams ${MVOUTLETSTOSTRMFILES})
add_executable (pitremove ${PITREMOVE})
add_executable (threshold ${THRESHOLD})
add_executable (curvature ${CURVATURE})
add_executable (d8distuptoridge ${D8DISTUP})
add_executable (fuzzyslpposinference ${FUZSLPPOSINF})
add_executable (hardenslppos ${HARDENSLPPOS})
add_executable (selecttyplocslppos ${TYPLOCSEL})
add_executable (simplecalculator ${CALCULATOR})


install(TARGETS aread8 
                areadinf
                d8flowdir
                d8distdowntostream
                dinfdistuptoridge
                dinfflowdir
                dropanalysis
                moveoutletstostreams
                pitremove
                threshold
				curvature
				d8distuptoridge
				fuzzyslpposinference
				hardenslppos
				selecttyplocslppos
				simplecalculator
        DESTINATION bin)

