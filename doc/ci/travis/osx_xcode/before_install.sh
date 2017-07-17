#!/bin/sh

set -e
brew update
# install openmpi
brew list openmpi &>/dev/null || brew install openmpi
# or install mpich2
# however mpich2 will cause link error: ld: unknown option: -headerpad_max_install_names;
# which is because there is a semicolon after flag -headerpad_max_install_names
#  see details in https://github.com/OSGeo/homebrew-osgeo4mac/issues/216
#brew install mpich2
