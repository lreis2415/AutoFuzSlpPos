#!/bin/sh

set -e
cd autofuzslppos
mkdir bin
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DINSTALL_PREFIX=../bin
make -j4
sudo make install
cd ..
# list all executable file
cd bin
ls
