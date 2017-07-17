#!/bin/sh

set -e
brew update
# install openmpi, be aware, mpich2 got error on macOS!
#brew install mpich2
brew list openmpi &>/dev/null || brew install openmpi
