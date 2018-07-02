#!/bin/bash

# this version of build builds with all programs with afl-clang-fast, modified with LAF (https://lafintel.wordpress.com/)
BUILD="laf"
PREFIX=""

mkdir projects
mkdir targets
mkdir results
cd projects
mkdir $BUILD
cd $BUILD

# set env variables for laf
export LAF_SPLIT_SWITCHES=1
export LAF_TRANSFORM_COMPARES=1
export LAF_SPLIT_COMPARES=1
export CC=~/fuzzing/laf/afl-clang-fast 
export CXX=~/fuzzing/laf/afl-clang-fast++

# Currently 5 crafted challenge binaries + 25 Real Binaries in different vulnerable versions

# custom examples
git clone https://github.com/xct-r3v3rse/challenges.git
cd challenges
./build.sh
cd ..
mkdir -p ../../targets/$BUILD/challenges
ln -s ../../../projects/$BUILD/challenges/build64/000 ../../targets/$BUILD/challenges/000 
ln -s ../../../projects/$BUILD/challenges/build64/002 ../../targets/$BUILD/challenges/002
ln -s ../../../projects/$BUILD/challenges/build64/003 ../../targets/$BUILD/challenges/003
ln -s ../../../projects/$BUILD/challenges/build64/004 ../../targets/$BUILD/challenges/004
ln -s ../../../projects/$BUILD/challenges/build64/005 ../../targets/$BUILD/challenges/005

# libtiff
git clone https://gitlab.com/libtiff/libtiff.git
cd libtiff 
git checkout Release-v4-0-3
$PREFIX ./configure LDFLAGS="-static"
make -j4
cd ..
mkdir -p ../../targets/$BUILD/libtiff
ln -s ../../../projects/$BUILD/libtiff/tools/tiffinfo ../../targets/$BUILD/libtiff/tiffinfo # -i -z @@
ln -s ../../../projects/$BUILD/libtiff/tools/pal2rgb ../../targets/$BUILD/libtiff/pal2rgb # -c none @@ out
ln -s ../../../projects/$BUILD/libtiff/tools/raw2tiff ../../targets/$BUILD/libtiff/raw2tiff # -c none @@ out


# libjpeg-turbo
wget https://kent.dl.sourceforge.net/project/libjpeg-turbo/1.5.0/libjpeg-turbo-1.5.0.tar.gz
tar -xvf libjpeg-turbo-1.5.0.tar.gz
cd libjpeg-turbo-1.5.0
$PREFIX ./configure LDFLAGS="-static"
make -j4
cd ..
mkdir -p ../../targets/$BUILD/libjpeg-turbo
ln -s ../../../projects/$BUILD/libjpeg-turbo-1.5.0/cjpeg ../../targets/$BUILD/libjpeg-turbo/cjpeg
ln -s ../../../projects/$BUILD/libjpeg-turbo-1.5.0/djpeg ../../targets/$BUILD/libjpeg-turbo/djpeg
ln -s ../../../projects/$BUILD/libjpeg-turbo-1.5.0/rdjpgcom ../../targets/$BUILD/libjpeg-turbo/rdjpgcom
ln -s ../../../projects/$BUILD/libjpeg-turbo-1.5.0/jpegtran ../../targets/$BUILD/libjpeg-turbo/jpegtran


# libpng
wget https://download.sourceforge.net/libpng/libpng-1.6.17.tar.gz
tar -xvf libpng-1.6.17.tar.gz
cd libpng-1.6.17
$PREFIX ./configure LDFLAGS="-static"
make -j4
cd ..
mkdir -p ../../targets/$BUILD/libpng
ln -s ../../../projects/$BUILD/libpng-1.6.17/pngfix ../../targets/$BUILD/libpng/pngfix
ln -s ../../../projects/$BUILD/libpng-1.6.17/pngimage ../../targets/$BUILD/libpng/pngimage


# libming 
git clone https://github.com/libming/libming.git
cd libming
git checkout ming-0_4_8
./autogen.sh
$PREFIX ./configure LDFLAGS="-static"
make -j4
make clean # no idea why cleaning and rebuilding is needed but it doesnt work without
make 
cd ..
mkdir -p ../../targets/$BUILD/libming
ln -s ../../../projects/$BUILD/libming/util/swftocxx ../../targets/$BUILD/libming/swftocxx
ln -s ../../../projects/$BUILD/libming/util/swftophp ../../targets/$BUILD/libming/swftophp
ln -s ../../../projects/$BUILD/libming/util/swftoperl ../../targets/$BUILD/libming/swftoperl
ln -s ../../../projects/$BUILD/libming/util/swftopython ../../targets/$BUILD/libming/swftopython
ln -s ../../../projects/$BUILD/libming/util/listjpeg ../../targets/$BUILD/libming/listjpeg
ln -s ../../../projects/$BUILD/libming/util/listmp3 ../../targets/$BUILD/libming/listmp3
ln -s ../../../projects/$BUILD/libming/util/listswf ../../targets/$BUILD/libming/listswf
ln -s ../../../projects/$BUILD/libming/util/raw2adpcm ../../targets/$BUILD/libming/raw2adpcm


# libjasper ###########################################
mkdir jasper
mkdir jasper/build
git clone https://github.com/mdadams/jasper.git jasper/src
cd jasper/src
git checkout version-1.900.1
cd ../build
$PREFIX ../src/configure "LDFLAGS=-static"
#cmake -DJAS_ENABLE_SHARED=OFF ../src # this is for current versions
make -j4
cd ../..
mkdir -p ../../targets/$BUILD/jasper
ln -s ../../../projects/$BUILD/jasper/build/src/appl/imginfo ../../targets/$BUILD/jasper/imginfo
ln -s ../../../projects/$BUILD/jasper/build/src/appl/imgcmp ../../targets/$BUILD/jasper/imgcmp
ln -s ../../../projects/$BUILD/jasper/build/src/appl/jasper ../../targets/$BUILD/jasper/jasper

# libyaml ###########################################
git clone https://github.com/yaml/libyaml.git libyaml
cd libyaml
git checkout 0.1.5
./bootstrap
$PREFIX ./configure "LDFLAGS=-static"
make -j4
cd ..
mkdir -p ../../targets/$BUILD/libyaml
ln -s ../../../projects/$BUILD/libyaml/tests/run-scanner ../../targets/$BUILD/libyaml/run-scanner


# giflib ###########################################
git clone https://github.com/rcancro/giflib.git giflib
cd giflib
git checkout 5.1.1
./autogen.sh
$PREFIX ./configure "LDFLAGS=-static"
make -j4
cd ..
mkdir -p ../../targets/$BUILD/giflib
ln -s ../../../projects/$BUILD/giflib/util/giftext ../../targets/$BUILD/giflib/giftext
ln -s ../../../projects/$BUILD/giflib/util/giffix ../../targets/$BUILD/giflib/giffix
ln -s ../../../projects/$BUILD/giflib/util/gif2rgb ../../targets/$BUILD/giflib/gif2rgb
ln -s ../../../projects/$BUILD/giflib/util/gifclrmp ../../targets/$BUILD/giflib/gifclrmp
