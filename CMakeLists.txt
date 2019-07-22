# ----------------------------------------------------------------------------
#  Root CMake file for AutoFuzSlpPos.
#
#     Please from the off-tree build directory, invoke:
#       $ cmake <path/to/AutoFuzSlpPos>
#
#       Optional cmake options:
#         -DINSTALL_PREFIX=<path/to/install>
#         -DLLVM_ROOT_DIR Specific the root directory of brew installed LLVM, e.g., /usr/local/opt/llvm
#
#  Routine testing platforms and compilers include:
#     1. Windows 10 with Visual Studio 2010/2015, mongo-c-driver-1.5.5, GDAL-1.11.4/2.4.1
#     2. Windows 10 with msys2/mingw64 (GCC-8.2.0), mongo-c-driver-1.6.1, GDAL-2.3.2
#     3. CentOS 6.2 (cluster) with GCC-4.8.4, mongo-c-driver-1.5.5, GDAL-1.9.0
#     4. Red Hat Server 6.2 (cluster) with ICC-12.1.0, mongo-c-driver-1.6.1, GDAL-1.11.5 (Without UnitTest)
#     5. macOS 10.14.5 with Clang-10.0 with Xcode, mongo-c-driver-1.14.0, GDAL-2.4.2 (brew installed)
#     6. Windows 10 with Visual Studio 2013+Intel C++ Compiler 17.0, mongo-c-driver-1.5.5, GDAL-1.11.4
#
#  Created and maintained by Liangjun Zhu (zlj@lreis.ac.cn)
#  Latest updated: Jul. 20, 2019
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
