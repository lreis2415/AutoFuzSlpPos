#!/bin/sh

set -e
mkdir -p autofuzslppos_osx_gcc/autofuzslppos/bin
cd autofuzslppos
mkdir build
cd build
# Be caution, the absolute path should be used in INSTALL_PREFIX!
cmake .. -DOPENMP=1 -DCMAKE_BUILD_TYPE=Release -DINSTALL_PREFIX=/Users/travis/build/lreis2415/AutoFuzSlpPos/autofuzslppos_osx_gcc/autofuzslppos/bin
make -j4
sudo make install
cd ../..
ls
# copy python scripts
cp autofuzslppos/*.py autofuzslppos_osx_gcc/autofuzslppos
# copy data, test, and manual to release directory
cp -R data autofuzslppos_osx_gcc/autofuzslppos/data
cp -R test autofuzslppos_osx_gcc/autofuzslppos/test
cp *.pdf autofuzslppos_osx_gcc/autofuzslppos
# zip
zip -r autofuzslppos_osx_gcc.zip autofuzslppos_osx_gcc
# list release files
cd autofuzslppos_osx_gcc
ls
