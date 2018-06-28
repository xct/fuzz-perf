# fuzz-perf
Framework that evaluates fuzzers by comparing achieved code coverage and found bugs. At this point there are 5 challenge binaries and 25 real programs in various vulnerable versions.

The coverage data is mostly filtered to the source directory of the application. This includes files that are possible not part of the particular tool inside a tested set of tools. At some point in the future we could look at the makefiles and make more specific filters, to get higher coverage per application. However this does not change the relative results and does not impede the comparison.

## Requirements
* lcov (using genhtml to get readable coverage information)
* php php-dev

## Setup

* run build.sh to download, build & symlink the target programs
* config.ini: adjust paths to your local dynamorio installation 
* config.ini: adjust runtime value (how long each fuzzer is executed in minutes)
* config.ini: adjust which fuzzer drivers to include in the test
* run `python3 perf.py` and wait for the results

## Add own fuzzer
* to add an own fuzzer you need to implement a class in drivers.py for your fuzzer
* just copy one of the other fuzzers and adjust paths / call command line to accomodate for your fuzzer 

## Troubleshoot
* if your fuzzer needs a virtualenv you need to code that into the driver or activate it before running this 

## Example-Output

```
Programm & afl & pathfinder & pathfinder_hybrid
 000 & 4.8% & 4.8% & 4.8%
 002 & 4.8% & 4.8% & 4.8%
 003 & 4.9% & 5.0% & 4.9%
 004 & 4.9% & 4.5% & 5.0%
 005 & 5.0% & 4.5% & 4.9%
 giftext & 23.5% & 28.4% & 23.7%
 gif2rgb & 10.9% & 16.4% & 10.9%
 giffix & 23.0% & 22.2% & 25.9%
 gifclrmp & 13.5% & 12.9% & 13.5%
 imginfo & 5.6% & 2.5% & 3.1%
 imgcmp & 5.7% & 2.6% & 3.0%
 jasper & 6.3% & 5.3% & 3.4%
 run-scanner & 52.8% & 19.1% & 51.1%
 swftocxx & 5.3% & 4.8% & 5.0%
 swftophp & 4.8% & 4.8% & 5.0%
 swftoperl & 4.5% & 4.7% & 5.3%
 listjpeg & 4.6% & 4.6% & 4.6%
 listmp3 & 4.6% & 4.6% & 4.6%
 listswf & 5.6% & 5.2% & 5.0%
 raw2adpcm & 5.0% & 5.0% & 5.0%
 pngimage & 3.6% & 4.3% & 3.6%
 pngfix & 3.9% & 3.8% & 3.9%
 cjpeg & 5.2% & 5.1% & 5.2%
 djpeg & 4.9% & 4.9% & 4.8%
 rdjpgcom & 5.3% & 5.5% & 5.4%
 jpegtran & 5.0% & 4.9% & 4.9%
 tiffinfo & 4.4% & 4.2% & 4.1%
 pal2rgb & 4.0% & 4.0% & 4.1%
 raw2tiff & 4.9% & 4.6% & 4.6%

Crashes:
Programm & afl & pathfinder & pathfinder_hybrid
 000 & 0 & 1 & 1
 002 & 0 & 1 & 1
 003 & 1 & 1 & 2
 004 & 0 & 0 & 0
 005 & 0 & 0 & 0
 giftext & 0 & 0 & 4
 gif2rgb & 0 & 0 & 0
 giffix & 0 & 2 & 1
 gifclrmp & 1 & 1 & 2
 imginfo & 0 & 0 & 0
 imgcmp & 0 & 0 & 0
 jasper & 0 & 0 & 0
 run-scanner & 0 & 0 & 0
 swftocxx & 0 & 0 & 0
 swftophp & 0 & 0 & 0
 swftoperl & 0 & 0 & 0
 listjpeg & 0 & 0 & 0
 listmp3 & 0 & 0 & 0
 listswf & 0 & 0 & 0
 raw2adpcm & 0 & 0 & 0
 pngimage & 0 & 0 & 0
 pngfix & 0 & 0 & 0
 cjpeg & 0 & 0 & 0
 djpeg & 0 & 0 & 0
 rdjpgcom & 0 & 0 & 0
 jpegtran & 0 & 0 & 0
 tiffinfo & 0 & 0 & 0
 pal2rgb & 0 & 0 & 0
 raw2tiff & 1 & 0 & 0


Done!
```