# fuzz-perf
framework that evaluates fuzzers by comparing achieved code coverage and found bugs.


## General
* early development version, might not work for you.
* adding more and more target programs to build.sh overtime, at this points its just very few

## Requirements

* lcov (using genhtml to get readable coverage information)

## Setup

* run build.sh to download, build & symlink the target programs
* config.ini: adjust paths to your local dynamorio installation 
* adjust runtime value in config.ini (how long each fuzzer is executed)
* adjust which fuzzer drivers to include in the test
* run `python3 perf.py` and wait for the results

## Add own fuzzer

* to add an own fuzzer you need to implement a class in drivers.py for your fuzzer (very easy)
* just copy one of the other fuzzers and adjust paths / call command line to accomodate for your fuzzer 


## Example-Output

```
Results: (Runtime=10)
{'afl': [('giftext', '39.5'), ('run-scanner', '58.4'), ('imginfo', '9.2')], 'Pathfinder': [('giftext', '34.8'), ('run-scanner', '29.7'), ('imginfo', '13.6')]}
```