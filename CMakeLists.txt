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
#  Created and maintained by Liangjun Zhu (zlj@lreis.ac.cn)
#  Latest updated: Oct. 28, 2023
#  Copyright (C) 2015-2023 Lreis, IGSNRR, CAS
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
    SET(INSTALL_DIR ${INSTALL_PREFIX} CACHE PATH "Set specified install path" FORCE)
ELSE()
    IF (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
        SET(INSTALL_DIR ${PROJECT_BINARY_DIR} CACHE PATH "Set specified install path" FORCE)
    ELSE ()
        SET(INSTALL_DIR ${CMAKE_INSTALL_PREFIX} CACHE PATH "Set default install path" FORCE)
    ENDIF ()
ENDIF ()
SET(INSTALL_PREFIX ${INSTALL_DIR} CACHE PATH "Set INSTALL_PREFIX cache" FORCE)
SET(CMAKE_INSTALL_PREFIX ${INSTALL_DIR} CACHE PATH "Set CMAKE_INSTALL_PREFIX cache" FORCE)

SET(TAUDEM_ALL ${CMAKE_CURRENT_SOURCE_DIR}/autofuzslppos/taudem_ext)

ADD_SUBDIRECTORY(${TAUDEM_ALL})
