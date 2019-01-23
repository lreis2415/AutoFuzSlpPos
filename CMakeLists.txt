# ----------------------------------------------------------------------------
#  Root CMake file for AutoFuzSlpPos.
#
#     Please from the off-tree build directory, invoke:
#       $ cmake <path/to/AutoFuzSlpPos>
#
#  Routine testing platforms and compilers include:
#     1. Windows 10 with Visual Studio 2013, MSMPI-v8
#     2. Windows 10 with mingw64 (GCC-4.9.3), MSMPI-v8
#     3. CentOS 6.2 (cluster) with GCC-4.8.4, MPICH-3.1.4
#     4. Red Hat Server 6.2 (cluster) with ICC-12.1.0, Intel MPI 4.0
#     5. macOS 10.12.6 with Clang-8.0 (or GCC-4.9.3), OpenMPI-1.10.4
#
#  Created and maintained by Liang-Jun Zhu (zlj@lreis.ac.cn)
#  Latest updated: Jan. 22, 2019
#  Copyright (C) 2015-2019 Lreis, IGSNRR, CAS
# ----------------------------------------------------------------------------
### Disable in-source builds to prevent source tree corruption.
IF(" ${CMAKE_SOURCE_DIR}" STREQUAL " ${CMAKE_BINARY_DIR}")
  MESSAGE(FATAL_ERROR "
FATAL: In-source builds are not allowed.
       You should create a separate directory for build files."
)
ENDIF()
CMAKE_MINIMUM_REQUIRED(VERSION 3.1 FATAL_ERROR)
if(POLICY CMP0015)
    cmake_policy(SET CMP0015 NEW)
endif()
if(POLICY CMP0054)
    cmake_policy(SET CMP0054 NEW)
endif()
if(POLICY CMP0074)
    cmake_policy(SET CMP0074 NEW)
endif()

# Set initial project name with coding languages
PROJECT(AutoFuzSlpPos CXX C)

### Set default or specified installation directory.
IF (INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX ${INSTALL_PREFIX} CACHE PATH "Set specified install path" FORCE)
ELSEIF(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  SET(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR}/bin CACHE PATH "Set default install path" FORCE)
ENDIF ()
SET(INSTALL_DIR ${CMAKE_INSTALL_PREFIX})

### In case of Makefiles if the user does not setup CMAKE_BUILD_TYPE, assume it's Release.
IF(CMAKE_GENERATOR MATCHES "Makefiles|Ninja" AND "${CMAKE_BUILD_TYPE}" STREQUAL "")
  SET(CMAKE_BUILD_TYPE Release)
ENDIF()

### Allow project folders in MSVC and Xcode.
IF(MSVC OR XCODE)
  SET_PROPERTY(GLOBAL PROPERTY USE_FOLDERS ON)
ENDIF()

### Break in case of popular CMake configuration mistakes.
IF(NOT CMAKE_SIZEOF_VOID_P GREATER 0)
  MESSAGE(FATAL_ERROR "CMake fails to determine the bitness of the target platform.
  Please check your CMake and compiler installation."
)
ENDIF()

SET(TAUDEM_ALL ${CMAKE_CURRENT_SOURCE_DIR}/autofuzslppos/taudem_ext)
ADD_SUBDIRECTORY(${TAUDEM_ALL})

### Auxiliary.
STATUS("")
STATUS("  Install path:" ${CMAKE_INSTALL_PREFIX})
STATUS("")
