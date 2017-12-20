#!/bin/sh

set -e
mkdir -p autofuzslppos_linux_gcc48/autofuzslppos/bin
mkdir build
cd build
# Be caution, the absolute path should be used in INSTALL_PREFIX!
cmake .. -DOPENMP=1 -DCMAKE_BUILD_TYPE=Release -DINSTALL_PREFIX=/home/travis/build/lreis2415/AutoFuzSlpPos/autofuzslppos_linux_gcc48/autofuzslppos/bin
make -j4
sudo make install
cd ../..
ls
# copy python scripts
cp autofuzslppos/*.py autofuzslppos_linux_gcc48/autofuzslppos
# copy data, test, and manual to release directory
cp -R data autofuzslppos_linux_gcc48/autofuzslppos/data
cp -R test autofuzslppos_linux_gcc48/autofuzslppos/test
cp *.pdf autofuzslppos_linux_gcc48/autofuzslppos
# zip
zip -r autofuzslppos_linux_gcc48.zip autofuzslppos_linux_gcc48
# list release files
cd autofuzslppos_linux_gcc48
ls
