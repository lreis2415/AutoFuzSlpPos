set(shape_srcs ${TAUDEM_SRC}/ReadOutlets.cpp)
set(common_srcs ${TAUDEM_SRC}/commonLib.cpp ${TAUDEM_SRC}/tiffIO.cpp)
# Adds include directories in such a way that directories from the TauDEM source tree go first.
geo_include_directories(${TAUDEM_SRC})

set(D8DISTUP D8DistUpToRidge.cpp D8DistUpToRidgemn.cpp ${common_srcs})
set(DINFDISTUP DinfDistUpToRidge.cpp DinfDistUpToRidgemn.cpp ${common_srcs})
set(FUZSLPPOSINF FuzzySlpPosInference.cpp FuzzySlpPosInferencemn.cpp ${common_srcs})
set(HARDENSLPPOS HardenSlpPos.cpp HardenSlpPosmn.cpp ${common_srcs})
set(TYPLOCSEL stats.cpp SelectTypLocSlpPos.cpp SelectTypLocSlpPosmn.cpp ${common_srcs})
set(CALCULATOR SimpleCalculator.cpp SimpleCalculatormn.cpp ${common_srcs})
set(RPISKIDMORE RPISkidmore.cpp RPISkidmoremn.cpp ${common_srcs})
set(RIDGEEXTRACTION stats.cpp RidgeExtraction.cpp RidgeExtractionmn.cpp ${common_srcs})

add_executable(d8distuptoridge ${D8DISTUP})
add_executable(dinfdistuptoridge ${DINFDISTUP})
add_executable(fuzzyslpposinference ${FUZSLPPOSINF})
add_executable(hardenslppos ${HARDENSLPPOS})
add_executable(selecttyplocslppos ${TYPLOCSEL})
add_executable(simplecalculator ${CALCULATOR})
add_executable(rpiskidmore ${RPISKIDMORE})
add_executable(ridgeextraction ${RIDGEEXTRACTION})

set(SLPPOS_APP
        d8distuptoridge
        dinfdistuptoridge
        fuzzyslpposinference
        hardenslppos
        selecttyplocslppos
        simplecalculator
        rpiskidmore
        ridgeextraction
        )

# third-party programs based on TauDEM framework
foreach (c_target ${SLPPOS_APP})
    target_link_libraries(${c_target} ${MPI_LIBRARIES} ${GDAL_LIBRARIES})
    install(TARGETS ${c_target} DESTINATION ${INSTALL_DIR})
    IF (MSVC)
        SET_PROPERTY(TARGET ${c_target} PROPERTY FOLDER "AutoFuzSlpPos")
    ENDIF ()
endforeach (c_target ${SLPPOS_APP})
