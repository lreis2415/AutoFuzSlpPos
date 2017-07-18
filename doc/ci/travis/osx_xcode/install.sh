#!/bin/sh

set -e
mkdir -p autofuzslppos_osx_xcode/autofuzslppos/bin
cd autofuzslppos
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DINSTALL_PREFIX=../../autofuzslppos_osx_xcode/autofuzslppos/bin
make -j4
sudo make install
cd ../..
ls
# copy python scripts
cp autofuzslppos/*.py autofuzslppos_osx_xcode/autofuzslppos
# copy data, test, and manual to release directory
cp -R data autofuzslppos_osx_xcode/autofuzslppos/data
cp -R test autofuzslppos_osx_xcode/autofuzslppos/test
cp *.pdf autofuzslppos_osx_xcode/autofuzslppos
# zip
zip -r autofuzslppos_osx_xcode.zip autofuzslppos_osx_xcode
# list release files
cd autofuzslppos_osx_xcode
ls
