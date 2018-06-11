#!/bin/bash

# this script sets the programs and versions used as targets in the master thesis
# this creates a projects directory at the folder level where pathfinders folder is

mkdir projects
mkdir targets
mkdir results
cd projects


# libjpeg-turbo
wget https://kent.dl.sourceforge.net/project/libjpeg-turbo/1.5.0/libjpeg-turbo-1.5.0.tar.gz
tar -xvf libjpeg-turbo-1.5.0.tar.gz
cd libjpeg-turbo-1.5.0
./configure LDFLAGS="-static"
make -j4
cd ..
mkdir ../targets/libjpeg-turbo
mkdir ../results/libjpeg-turbo
ln -s ../../projects/libjpeg-turbo-1.5.0/cjpeg ../targets/libjpeg-turbo/cjpeg
ln -s ../../projects/libjpeg-turbo-1.5.0/djpeg ../targets/libjpeg-turbo/djpeg
ln -s ../../projects/libjpeg-turbo-1.5.0/rdjpgcom ../targets/libjpeg-turbo/rdjpgcom
ln -s ../../projects/libjpeg-turbo-1.5.0/jpegtran ../targets/libjpeg-turbo/jpegtran


# libpng
wget https://download.sourceforge.net/libpng/libpng-1.6.17.tar.gz
tar -xvf libpng-1.6.17.tar.gz
cd libpng-1.6.17
./configure LDFLAGS="-static"
make -j4
cd ..
mkdir ../targets/libpng
mkdir ../results/libpng
ln -s ../../projects/libpng-1.6.17/pngfix ../targets/libpng/pngfix
ln -s ../../projects/libpng-1.6.17/pngimage ../targets/libpng/pngimage


# libming 
git clone https://github.com/libming/libming.git
cd libming
git checkout ming-0_4_8
./autogen.sh
./configure LDFLAGS="-static"
make -j4
cd ..
mkdir ../targets/libming
mkdir ../results/libming
ln -s ../../projects/libming/util/swftocxx ../targets/libming/swftocxx
ln -s ../../projects/libming/util/swftophp ../targets/libming/swftophp
ln -s ../../projects/libming/util/swftoperl ../targets/libming/swftoperl
ln -s ../../projects/libming/util/swftopython ../targets/libming/swftopython
ln -s ../../projects/libming/util/listjpeg ../targets/libming/listjpeg
ln -s ../../projects/libming/util/listmp3 ../targets/libming/listmp3
ln -s ../../projects/libming/util/listswf ../targets/libming/listswf


# libjasper ###########################################
mkdir jasper
mkdir jasper/build
git clone https://github.com/mdadams/jasper.git jasper/src
cd jasper/src
git checkout version-1.900.1
cd ../build
../src/configure "LDFLAGS=-static"
#cmake -DJAS_ENABLE_SHARED=OFF ../src # this is for current versions
make -j4
cd ../..
mkdir ../targets/jasper
mkdir ../results/jasper
ln -s ../../projects/jasper/build/src/appl/imginfo ../targets/jasper/imginfo


# libyaml ###########################################
git clone https://github.com/yaml/libyaml.git libyaml
cd libyaml
git checkout 0.1.5
./bootstrap
./configure "LDFLAGS=-static"
make -j4
cd ..
mkdir ../targets/libyaml
mkdir ../results/libyaml
ln -s ../../projects/libyaml/tests/run-scanner ../targets/libyaml/run-scanner


# giflib ###########################################
git clone https://github.com/rcancro/giflib.git giflib
cd giflib
git checkout 5.1.1
./autogen.sh
./configure "LDFLAGS=-static"
make -j4
cd ..
mkdir ../targets/giflib
mkdir ../results/giflib
ln -s ../../projects/giflib/util/giftext ../targets/giflib/giftext
