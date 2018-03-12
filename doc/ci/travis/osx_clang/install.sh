#!/bin/sh

set -e
mkdir -p autofuzslppos_osx_clang/autofuzslppos/bin
mkdir build
cd build
# Be caution, the absolute path should be used in INSTALL_PREFIX!
cmake .. -DOPENMP=1 -DCMAKE_BUILD_TYPE=Release -DINSTALL_PREFIX=/Users/travis/build/lreis2415/AutoFuzSlpPos/autofuzslppos_osx_clang/autofuzslppos/bin
make -j4
sudo make install
cd ..
ls
# copy python scripts
cp autofuzslppos/*.py autofuzslppos_osx_clang/autofuzslppos
# copy data, test, and manual to release directory
cp -R data autofuzslppos_osx_clang/autofuzslppos/data
#cp -R test autofuzslppos_osx_clang/autofuzslppos/test
# zip
zip -r autofuzslppos_osx_clang.zip autofuzslppos_osx_clang
# list release files
cd autofuzslppos_osx_clang
ls
