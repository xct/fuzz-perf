import drivers
import time
import subprocess
import psutil
import sys
import json
import re
import random
from configparser import ConfigParser

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


class Perf():

    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        bits = config.get('General','Arch')
        self.drivers = []
        self.coverage = {}
        drivers = config.items("Drivers")
        print("Loading Drivers...")
        for k, v in drivers:   
            print(v)         
            instance = getattr(sys.modules["drivers"], v)()
            self.drivers.append(instance)
            self.coverage[instance.name] = []
        self.runtime = int(config.get('General','Runtime')) # time in minutes to run every of the fuzzers
        self.drrun = config.get('General', 'DynamoRIO_'+bits)+'/bin'+bits+'/drrun'
        self.drcov2lcov = config.get('General', 'DynamoRIO_'+bits)+'/clients/bin'+bits+'/drcov2lcov'
        self.targets = json.loads(config.get('General','Targets'))      
        self.filters = json.loads(config.get('General','Filters'))
        # some cleanup
        self.run("rm -rf results/*")
        self.coverage_by_target = dict()
        self.crashes_by_target = dict()


    def run(self, cmd):
        print(cmd)
        proc = subprocess.Popen(cmd, shell=True)
        try:
            proc.wait(timeout=self.runtime*60)
        except subprocess.TimeoutExpired:
            kill(proc.pid)


    def runs(self, cmd):
        s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
        print(s)
        return s.decode("utf-8") # otherwise its a bytes literal


    def write_results(self):
        with open('results/summary.txt', 'w') as outfile:
            outfile.write(json.dumps(self.coverage)) 


    def print_coverage_latex(self):
        print("Coverage:")
        #Beispiel 002 & 4(0) & 4(0) & 4(1) & 8(6)
        result = "Programm"
        for driver in self.drivers:
            result += " & " + driver.name
        result += "\n"
        for name in self.coverage_by_target:
            result += " "+name
            for driver, value in self.coverage_by_target[name]:
                result +=  " & " + str(value) + "%"
            result += "\n"
        print(result) 


    def print_crashes_latex(self):
        print("Crashes:")
        result = "Programm"
        for driver in self.drivers:
            result += " & " + driver.name 
        result += "\n"
        for name in self.crashes_by_target:
            result += " "+name
            for driver, value in self.crashes_by_target[name]:
                result +=  " & " + value.replace("\n","")
            result += "\n"
        print(result)


    def main(self):
        # 0. build target applications (at this point we require that has been done with ./build.sh)
        # 1. run with fuzzers
        print("Running Fuzzers & Generating Coverage...")
        print(self.drivers)
        print(self.targets)

        for driver in self.drivers: # array of fuzzers
            for project, targets in self.targets.items(): # project | dict of targets with their arguments
                for entry in targets:
                    target = random.choice(list(entry.keys())) # there is only one
                    raw_args = entry[target]
                    # run the fuzzer for the specified time
                    self.run(driver.pre(project, target, raw_args))
                    self.run(driver.post())
                    # drcov
                    args = ""
                    for s in raw_args:
                        args += s.replace("@@","queue/$i")
                    cmd = "cd results/"+driver.name+"/"+project+"/"+target+" && "
                    cmd += "for i in `ls -1 queue/`; do "+self.drrun+" -t drcov -- ../../../../targets/"+project+"/"+target+" "+args+"; done"
                    self.run(cmd)
                    # drcov2lcov
                    cmd = "cd results/"+driver.name+"/"+project+"/"+target+" && "
                    cmd += self.drcov2lcov+" -dir . -output coverage.info"
                    if project in self.filters and len(self.filters[project]) > 0:
                        cmd += " --src_filter "+self.filters[project]
                    self.run(cmd)
                    # genhtml
                    cmd = "cd results/"+driver.name+"/"+project+"/"+target+" && "
                    cmd += "genhtml coverage.info --ignore-errors source --output-directory coverage"
                    s = self.runs(cmd)
                    p = re.search(r"lines......: ([0-9+\.[0-9]+)% \(", s).group(1)
                    self.coverage[driver.name].append((target, p))
                    if target not in self.coverage_by_target:
                        self.coverage_by_target[target] = []
                    self.coverage_by_target[target].append((driver.name, p))
                    # amount of crashes
                    if target not in self.crashes_by_target:
                        self.crashes_by_target[target] = []
                    self.crashes_by_target[target].append((driver.name, self.runs(driver.crashes())))

        # 2. generate results
        print("\nResults: (Runtime="+str(self.runtime)+")")
        print(self.coverage)
        print("\n")        
        self.write_results()
        self.print_coverage_latex()
        self.print_crashes_latex()
        print("\nDone!\n")


if __name__ == "__main__":
    if sys.version_info <= (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        sys.exit(1)
    perf = Perf()
    perf.main()