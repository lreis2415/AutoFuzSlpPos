# CMake build for multiply compilers under Windows, Linux, and macOS
# Author         : LiangJun Zhu
# Contact        : zlj@lreis.ac.cn
# Latest updated : July. 17, 2017
#
cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
SET(PRJNAME "AutoFuzSlpPos")
IF (COMMAND CMAKE_POLICY)
    CMAKE_POLICY(SET CMP0015 NEW)
ENDIF (COMMAND CMAKE_POLICY)
IF (ARCH EQUAL 64)
    SET(PRJNAME ${PRJNAME}_x64)
    IF (NOT WIN32)
        set(CMAKE_CXX_FLAG ${CMAKE_CXX_FLAG} "-m64")
    ENDIF ()
    MESSAGE(STATUS "64-bit version...")
ELSE ()
    SET(PRJNAME ${PRJNAME}_x32)
    MESSAGE(STATUS "32-bit version...")
ENDIF ()
PROJECT(${PRJNAME})
################# Install directory ##################
IF (INSTALL_PREFIX)
    SET(CMAKE_INSTALL_PREFIX ${INSTALL_PREFIX})
    SET(INSTALL_DIR ${INSTALL_PREFIX})
ELSE ()
    SET(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR})
    SET(INSTALL_DIR ${CMAKE_SOURCE_DIR}/bin)
ENDIF ()
################# OS platform   ##################
if (WIN32)
    add_definitions(-Dwindows)
    if (MSVC)
        add_definitions(-DMSVC)
    endif ()
elseif (APPLE)
    add_definitions(-Dmacos)
else ()
    add_definitions(-Dlinux)
endif ()
if (NOT MSVC)
    # Select flags.
    # refers to https://software.intel.com/en-us/articles/intel-cluster-toolkit-for-linux-error-when-compiling-c-aps-using-intel-mpi-library-compilation-driver-mpiicpc
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DMPICH_IGNORE_CXX_SEEK -DMPICH_SKIP_MPICXX")
    SET(CMAKE_CXX_FLAGS_RELWITHDEBINFO "-O2 -g")
    SET(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -fPIC -g -ggdb")
    SET(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O2 -Wall -fPIC")
endif ()
# Set a default build type for single-configuration
# CMake generators if no build type is set.
IF(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
   SET(CMAKE_BUILD_TYPE RelWithDebInfo)
ENDIF()
################# Find packages ##################
# MPI is required and OpenMP is optional.
# 1. MPI
IF (WIN32)
    IF (ARCH EQUAL 64)
        SET(MPI_LIB $ENV{MSMPI_LIB64})
    ELSE ()
        SET(MPI_LIB $ENV{MSMPI_LIB32})
    ENDIF ()
    SET(MPI_HOME $ENV{MSMPI_BIN})
    SET(MPI_INCLUDE_PATH $ENV{MSMPI_INC})
    SET(MPI_LIBRARIES ${MPI_LIB}\\msmpi.lib)
ELSE ()
    find_package(MPI REQUIRED)
    set(CMAKE_CXX_FLAG "${CMAKE_CXX_FLAG} ${MPI_COMPILE_FLAGS}")
    set(CMAKE_CXX_LINK_FLAGS "${CMAKE_CXX_LINK_FLAGS} ${MPI_LINK_FLAGS}")
ENDIF ()
IF (MPI_LIBRARIES)
    MESSAGE(STATUS "FOUND MPI: ${MPI_LIBRARIES}")
    INCLUDE_DIRECTORIES(${MPI_INCLUDE_PATH})
ENDIF ()
# 2. OpenMP
FIND_PACKAGE(OpenMP)
IF (OPENMP_FOUND)
    add_definitions(-DSUPPORT_OMP)
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
ENDIF ()
### Active C++11 standard, cross-platform. This requires CMake 3.1+
# SET(CMAKE_CXX_STANDARD 11) CMake may make mistake in intel c/c++ compiler
# 12.1, so make some test when setting the C++ Standard.
# refers to https://github.com/biicode/client/issues/10
include(CheckCXXCompilerFlag)
set(ENABLE_CXXFLAGS_TO_CHECK
    -std=gnu++11
    -std=c++11
    -std=gnu++0x
    -std=c++0x)
MESSAGE(STATUS "CHECK CXX STANDARD FLAGS...")
foreach(flag ${ENABLE_CXXFLAGS_TO_CHECK})
    string(REPLACE "-std=" "_" flag_var ${flag})
    string(REPLACE "+" "x" flag_var ${flag_var})
    check_cxx_compiler_flag("${flag}" COMPILER_HAS_CXX_FLAG${flag_var})
    if(COMPILER_HAS_CXX_FLAG${flag_var})
        MESSAGE(STATUS "${flag}...yes")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${flag}")
        break()
    endif()
endforeach()
MESSAGE(STATUS "USED CXX FLAGS: ${CMAKE_CXX_FLAGS}")
#################   step into subdirectories   ##################
SET(TAUDEM_SRC ./src)
IF(MSVC)
  SET_PROPERTY(GLOBAL PROPERTY USE_FOLDERS ON)
ENDIF()
ADD_SUBDIRECTORY(${TAUDEM_SRC})
### For CLion to implement the "make install" command
add_custom_target(install_${PRJNAME}
        $(MAKE) install
        DEPENDS ${PRJNAME}
        COMMENT "Installing ${PRJNAME}")
MESSAGE(STATUS "    Compiling AutoFuzSlpPos done")
