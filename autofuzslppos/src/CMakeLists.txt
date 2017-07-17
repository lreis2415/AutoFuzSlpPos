set(shape_srcs
        shapelib/shapefil.h
        shapelib/dbfopen.c
        shapelib/safileio.c
        shapelib/shpopen.c
        shapelib/shptree.c
        ReadOutlets.cpp)

#OBJFILES includes classes, structures, and constants common to all files
set(common_srcs commonLib.cpp tiffIO.cpp)

set(CONNECTDOWNFILES connectdownmn.cpp connectdown.cpp ${common_srcs} ${shape_srcs})
set(D8FILES aread8mn.cpp aread8.cpp ${common_srcs} ${shape_srcs})
set(DINFFILES areadinfmn.cpp areadinf.cpp ${common_srcs} ${shape_srcs})
set(D8 D8FlowDirmn.cpp d8.cpp Node.cpp ${common_srcs} ${shape_srcs})
set(D8DISTDOWN D8DistDownToStream.cpp D8DistDownToStreammn.cpp ${common_srcs})
set(DINFDISTDOWN DinfDistDown.cpp DinfDistDownmn.cpp ${common_srcs})
set(DINFDISTUP DinfDistUpToRidge.cpp DinfDistUpToRidgemn.cpp ${common_srcs})
set(DINF DinfFlowDirmn.cpp dinf.cpp Node.cpp ${common_srcs} ${shape_srcs})
set(PEUKERDOUGLAS PeukerDouglas.cpp PeukerDouglasmn.cpp ${common_srcs})
set(PITREMOVE flood.cpp PitRemovemn.cpp ${common_srcs})
set(DROPANALYSISFILES DropAnalysis.cpp DropAnalysismn.cpp ${common_srcs} ${shape_srcs})
set(MVOUTLETSTOSTRMFILES MoveOutletsToStrm.cpp MoveOutletsToStrmmn.cpp
        ${common_srcs} ${shape_srcs})
set(STREAMNET streamnet.cpp streamnetmn.cpp ${common_srcs} ${shape_srcs})
set(PITREMOVE flood.cpp PitRemovemn.cpp ${common_srcs})
set(THRESHOLD Threshold.cpp Thresholdmn.cpp ${common_srcs})
# Added by Liangjun Zhu, 2015/5/21
set(CURVATURE Curvature.cpp Curvaturemn.cpp ${common_srcs})
set(D8DISTUP D8DistUpToRidge.cpp D8DistUpToRidgemn.cpp ${common_srcs})
set(FUZSLPPOSINF FuzzySlpPosInference.cpp FuzzySlpPosInferencemn.cpp ${common_srcs})
set(HARDENSLPPOS HardenSlpPos.cpp HardenSlpPosmn.cpp ${common_srcs})
set(TYPLOCSEL stats.cpp SelectTypLocSlpPos.cpp SelectTypLocSlpPosmn.cpp ${common_srcs})
set(CALCULATOR SimpleCalculator.cpp SimpleCalculatormn.cpp ${common_srcs})
set(RPISKIDMORE RPISkidmore.cpp RPISkidmoremn.cpp ${common_srcs})
set(RIDGEEXTRACTION stats.cpp RidgeExtraction.cpp RidgeExtractionmn.cpp ${common_srcs})

add_executable(aread8 ${D8FILES})
add_executable(areadinf ${DINFFILES})
add_executable(connectdown ${CONNECTDOWNFILES})
add_executable(d8flowdir ${D8})
add_executable(d8distdowntostream ${D8DISTDOWN})
add_executable(dinfdistdown ${DINFDISTDOWN})
add_executable(dinfdistuptoridge ${DINFDISTUP})
add_executable(dinfflowdir ${DINF})
add_executable(peukerdouglas ${PEUKERDOUGLAS})
add_executable(dropanalysis ${DROPANALYSISFILES})
add_executable(moveoutletstostreams ${MVOUTLETSTOSTRMFILES})
add_executable(streamnet ${STREAMNET})
add_executable(pitremove ${PITREMOVE})
add_executable(threshold ${THRESHOLD})
add_executable(curvature ${CURVATURE})
add_executable(d8distuptoridge ${D8DISTUP})
add_executable(fuzzyslpposinference ${FUZSLPPOSINF})
add_executable(hardenslppos ${HARDENSLPPOS})
add_executable(selecttyplocslppos ${TYPLOCSEL})
add_executable(simplecalculator ${CALCULATOR})
add_executable(rpiskidmore ${RPISKIDMORE})
add_executable(ridgeextraction ${RIDGEEXTRACTION})

set(TAUDEM_TARGETS aread8
        areadinf
        connectdown
        d8flowdir
        d8distdowntostream
        dinfdistdown
        dinfdistuptoridge
        dinfflowdir
        peukerdouglas
        dropanalysis
        moveoutletstostreams
        streamnet
        pitremove
        threshold)

set(MY_TARGETS curvature
        d8distuptoridge
        fuzzyslpposinference
        hardenslppos
        selecttyplocslppos
        simplecalculator
        rpiskidmore
        ridgeextraction)
# TauDEM programs
foreach (c_target ${TAUDEM_TARGETS})
    target_link_libraries(${c_target} ${MPI_LIBRARIES})
    install(TARGETS ${c_target} DESTINATION ${INSTALL_DIR})
    IF (MSVC)
        SET_PROPERTY(TARGET ${c_target} PROPERTY FOLDER "TauDEM")
    ENDIF ()
endforeach (c_target ${TAUDEM_TARGETS})
# third-party programs based on TauDEM framework
foreach (c_target ${MY_TARGETS})
    target_link_libraries(${c_target} ${MPI_LIBRARIES})
    install(TARGETS ${c_target} DESTINATION ${INSTALL_DIR})
    IF (MSVC)
        SET_PROPERTY(TARGET ${c_target} PROPERTY FOLDER "AutoFuzSlpPos")
    ENDIF ()
endforeach (c_target ${MY_TARGETS})
