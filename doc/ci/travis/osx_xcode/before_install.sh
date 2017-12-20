#!/bin/sh

set -e
brew update
# Check if GDAL is already installed
brew list gdal &>/dev/null || brew install gdal
# install openmpi
brew list openmpi &>/dev/null || brew install openmpi
# or install mpich2
#brew install mpich2
