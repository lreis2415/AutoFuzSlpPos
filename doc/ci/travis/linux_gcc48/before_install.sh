#!/bin/sh

set -e
# update gcc to version 4.8
sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y
sudo apt-get update -qq
sudo apt-get install -qq gcc-4.8 g++-4.8
export CXX="g++-4.8" CC="gcc-4.8"
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 90
# install mpich2
sudo apt-get install -q libc-dev mpich2 libmpich2-dev
