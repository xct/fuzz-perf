# fuzz-perf
framework that evaluates fuzzers by comparing achieved code coverage and found bugs

## requirements

## Setup

* run build.sh to download, build & symlink the target programs
* adjust paths to your local dynamorio installation in config.ini
* adjust runtime value in config.ini (how long each fuzzer is executed)
* adjust which fuzzer drivers to include in the test
* run `python3 perf.py` and wait for the results

## Add own fuzzer

* to add an own fuzzer you need to implement a class in drivers.py for your fuzzer (very easy)
* just copy one of the other fuzzers and adjust paths / call command line to accomodate for your fuzzer 