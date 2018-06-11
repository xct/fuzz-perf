# fuzz-perf
framework that evaluates fuzzers by comparing achieved code coverage and found bugs.


## General
* early development version, might not work for you and needs adjustments to be used
* adding more and more target programs to build.sh overtime, at this points its just very few

## Requirements

* lcov (using genhtml to get readable coverage information)

## Setup

* run build.sh to download, build & symlink the target programs
* config.ini: adjust paths to your local dynamorio installation 
* config.ini: adjust runtime value (how long each fuzzer is executed)
* config.ini: adjust which fuzzer drivers to include in the test
* run `python3 perf.py` and wait for the results

## Add own fuzzer

* to add an own fuzzer you need to implement a class in drivers.py for your fuzzer (very easy)
* just copy one of the other fuzzers and adjust paths / call command line to accomodate for your fuzzer 


## Troubleshoot
* if your fuzzer needs a virtualenv you need to code that into the driver or activate it before running this 


## Example-Output

```
Results: (Runtime=1)
{'pathfinder': [('swftocxx', '4.5'), ('swftophp', '4.6'), ('swftoperl', '4.6'), ('listjpeg', '4.6'), ('listmp3', '4.6'), ('listswf', '5.2'), ('imginfo', '2.6'), ('giftext', '19.9'), ('pngimage', '4.2'), ('pngfix', '3.8'), ('run-scanner', '19.1')], 'afl': [('swftocxx', '5.2'), ('swftophp', '5.3'), ('swftoperl', '5.6'), ('listjpeg', '4.6'), ('listmp3', '4.6'), ('listswf', '5.0'), ('imginfo', '5.6'), ('giftext', '23.1'), ('pngimage', '3.6'), ('pngfix', '3.9'), ('run-scanner', '53.7')]}
Programm & afl & pathfinder
 run-scanner & 53.7 & 19.1
 giftext & 23.1 & 19.9
 listmp3 & 4.6 & 4.6
 pngimage & 3.6 & 4.2
 swftocxx & 5.2 & 4.5
 listjpeg & 4.6 & 4.6
 swftophp & 5.3 & 4.6
 listswf & 5.0 & 5.2
 swftoperl & 5.6 & 4.6
 imginfo & 5.6 & 2.6
 pngfix & 3.9 & 3.8
```