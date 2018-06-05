import drivers
import time
import subprocess
import psutil
import sys
import configparser

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

class Perf():

    def __init__(self):
        self.drivers = [drivers.PathfinderDriver(),] # list of fuzzers        
        self.runtime = 2 # time in minutes to run every of the fuzzers
        self.drrun = "/home/xct/fuzzing/dynamorio/build64/bin64/drrun"
        self.drcov2lcov = "/home/xct/fuzzing/dynamorio/build64/clients/bin64/drcov2lcov"

        self.targets = {}
        self.targets['libyaml'] = {'run-scanner' :["@@",]}
        self.targets['giflib'] = {'giftext' :["@@",]}
        self.targets['jasper'] = {'imginfo' :["-f @@",]}

        self.filters = {}
        self.filters['libyaml'] = 'yaml'
        self.filters['giflib'] = 'gif'
        self.filters['jasper'] = 'jasper'


    def run(self, cmd):
        print(cmd)
        proc = subprocess.Popen(cmd, shell=True)
        try:
            proc.wait(timeout=self.runtime*60)
        except subprocess.TimeoutExpired:
            kill(proc.pid)


    def main(self):
        # 0. build target applications (at this point we require that has been done with ./build.sh)
        # 1. run with fuzzers
        print("Running Fuzzers...")
        for driver in self.drivers: # array of fuzzers
            for project, targets in self.targets.items(): # project | dict of targets with their arguments
                for target in targets:
                    self.run(driver.pre(project, target, targets[target]))
                    self.run(driver.post())
                    pass
                 
        # 2. generate and save coverage data with fuzzer output
        print("Generating Coverage Data...")
        for driver in self.drivers: # array of fuzzers
            for project, targets in self.targets.items(): # project | dict of targets with their arguments
                for target in targets:
                    # drcov
                    cmd = "cd results/"+project+"/"+target+" && "
                    cmd += "for i in `ls -1 queue/`; do "+self.drrun+" -t drcov -- ../../../targets/"+project+"/"+target+" queue/$i; done"
                    self.run(cmd)
                    # drcov2lcov
                    cmd = "cd results/"+project+"/"+target+" && "
                    cmd += self.drcov2lcov+" -dir . -output coverage.info --src_filter "+self.filters[project]
                    self.run(cmd)
                    # genhtml
                    cmd = "cd results/"+project+"/"+target+" && "
                    cmd += "genhtml coverage.info --ignore-errors source --output-directory coverage"
                    self.run(cmd)


        # 3. generate results
        print("Results:")


if __name__ == "__main__":
    if sys.version_info <= (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        sys.exit(1)
    perf = Perf()
    perf.main()