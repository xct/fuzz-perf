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
